from rest_framework import serializers
from .models import Customer, User, Center, Plan, Slot, SlotBooking, Invoice


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get("email")).first()
        if user is None or not user.check_password(attrs.get("password")):
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    center_name = serializers.CharField(source='center.center_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email',
            'first_name', 'last_name', 'role',
            'center', 'center_name',
            'is_active', 'date_joined',
        ]
        read_only_fields = ['id', 'date_joined', 'center_name']

    def validate_role(self, value):
        if value not in ('super_admin', 'branch_user'):
            raise serializers.ValidationError("Role must be 'super_admin' or 'branch_user'.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    wave_display = serializers.CharField(source='get_wave_display', read_only=True)
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'mobile', 'email', 'center', 'plan', 'plan_name', 'wave', 'wave_display',
            'start_date', 'expiry_date', 'last_visit', 'status',
            'address', 'city', 'state', 'pincode', 'occupation', 'dob', 'created_at',
        ]

    def validate(self, attrs):
        center = attrs.get('center')
        mobile = attrs.get('mobile')
        email = attrs.get('email')
        instance = self.instance

        qs = Customer.objects.filter(center=center)
        if instance:
            qs = qs.exclude(pk=instance.pk)

        if mobile and qs.filter(mobile=mobile).exists():
            raise serializers.ValidationError({
                "mobile": "A customer with this phone number already exists in this branch."
            })
        if email and qs.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "A customer with this email already exists in this branch."
            })
        return attrs


class PlanSerializer(serializers.ModelSerializer):
    gst_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'plan_name', 'description', 'duration_months', 'price', 'gst_percentage', 'gst_amount', 'total_price', 'status']

    def get_gst_amount(self, obj):
        return round(float(obj.price) * float(obj.gst_percentage) / 100, 2)

    def get_total_price(self, obj):
        return round(float(obj.price) + self.get_gst_amount(obj), 2)

    def validate_plan_name(self, value):
        qs = Plan.objects.filter(plan_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A plan with this name already exists.")
        return value

    def validate_plan_name(self, value):
        qs = Plan.objects.filter(plan_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A plan with this name already exists.")
        return value


class CenterSerializer(serializers.ModelSerializer):
    total_customers = serializers.SerializerMethodField()

    class Meta:
        model = Center
        fields = ['id', 'center_name', 'location', 'mobile', 'email', 'poc_name', 'poc_contact', 'status', 'created_at', 'total_customers']
        read_only_fields = ['id', 'created_at', 'total_customers']

    def get_total_customers(self, obj):
        return obj.customer_set.count()

    def validate_center_name(self, value):
        qs = Center.objects.filter(center_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A center with this name already exists.")
        return value

    def validate_status(self, value):
        if value not in ('active', 'inactive'):
            raise serializers.ValidationError("Status must be 'active' or 'inactive'.")
        return value


class SlotSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source="center.center_name", read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['id', 'center', 'center_name', 'start_time', 'end_time', 'slot_time',
                  'booked_count', 'total_slot', 'status', 'is_enabled', 'created_at']
        read_only_fields = ['id', 'booked_count', 'created_at', 'slot_time', 'center_name']

    def validate_status(self, value):
        if value not in ('active', 'inactive'):
            raise serializers.ValidationError("Status must be 'active' or 'inactive'.")
        return value

    def get_slot_time(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"

    def validate(self, attrs):
        if attrs.get("start_time") and attrs.get("end_time") and attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError("End time must be greater than start time.")
        return attrs


class SlotBookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = ['id', 'customer', 'customer_name', 'slot', 'slot_time', 'booking_date', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'customer_name', 'slot_time']

    def get_slot_time(self, obj):
        return f"{obj.slot.start_time.strftime('%I:%M %p')} - {obj.slot.end_time.strftime('%I:%M %p')}"

    def validate(self, attrs):
        slot = attrs.get("slot")
        if not slot.is_enabled:
            raise serializers.ValidationError({"slot": "This slot is disabled."})
        if slot.booked_count >= slot.total_slot:
            raise serializers.ValidationError({"slot": "This slot is already full."})
        if SlotBooking.objects.filter(
            customer=attrs.get("customer"), slot=slot, booking_date=attrs.get("booking_date")
        ).exists():
            raise serializers.ValidationError({"non_field_errors": "This customer already booked this slot for this date."})
        return attrs

    def create(self, validated_data):
        booking = SlotBooking.objects.create(**validated_data)
        slot = validated_data["slot"]
        slot.booked_count += 1
        slot.save()
        return booking


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_id = serializers.CharField(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_id', 'center', 'customer', 'plan', 'amount', 'date', 'status', 'created_at']
        read_only_fields = ['id', 'invoice_id', 'created_at']
