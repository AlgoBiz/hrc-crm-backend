from rest_framework import serializers
from datetime import date
from dateutil.relativedelta import relativedelta
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


class CustomerCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id', 'center_name']


class CustomerPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'plan_name']


class CustomerInvoiceSerializer(serializers.ModelSerializer):
    invoice_id = serializers.CharField(read_only=True)
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)
    download_invoice_url = serializers.SerializerMethodField()
    gst_applied = serializers.SerializerMethodField()
    gst_amount = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_id', 'date', 'plan_name', 'amount', 'gst_applied', 'gst_amount', 'subtotal', 'status', 'download_invoice_url']

    def get_download_invoice_url(self, obj):
        return f'/api/invoices/{obj.id}/download/excel/'

    def get_gst_applied(self, obj):
        return obj.plan.gst if obj.plan else False

    def get_gst_amount(self, obj):
        if obj.plan and obj.plan.gst:
            return round(float(obj.amount) * 18 / 100, 2)
        return 0.0

    def get_subtotal(self, obj):
        gst_amount = self.get_gst_amount(obj)
        return round(float(obj.amount) + gst_amount, 2)


class CustomerSessionSerializer(serializers.ModelSerializer):
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = ['booking_date', 'slot_time', 'status']

    def get_slot_time(self, obj):
        return f"{obj.slot.start_time.strftime('%I:%M %p')} - {obj.slot.end_time.strftime('%I:%M %p')}"


class CustomerSerializer(serializers.ModelSerializer):
    plan = CustomerPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), source='plan', write_only=True
    )
    center = CustomerCenterSerializer(read_only=True)
    center_id = serializers.PrimaryKeyRelatedField(
        queryset=Center.objects.all(), source='center', write_only=True, required=False, allow_null=True
    )
    billing_history = CustomerInvoiceSerializer(source='invoices', many=True, read_only=True)
    sessions = CustomerSessionSerializer(source='slot_bookings', many=True, read_only=True)
    last_visit = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'mobile', 'email',
            'center', 'center_id',
            'plan', 'plan_id', 'wave',
            'start_date', 'expiry_date', 'last_visit', 'status',
            'address', 'city', 'state', 'pincode', 'occupation', 'dob', 'created_at',
            'billing_history', 'sessions',
        ]

    def get_last_visit(self, obj):
        latest_booking = obj.slot_bookings.order_by('-booking_date').first()
        return latest_booking.booking_date if latest_booking else None

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

    def create(self, validated_data):
        plan = validated_data.get('plan')
        if plan:
            start = date.today()
            validated_data['start_date'] = start
            validated_data['expiry_date'] = start + relativedelta(months=plan.duration_months)
        customer = Customer.objects.create(**validated_data)
        center = customer.center
        if plan and center:
            gst_amount = round(float(plan.price) * 18 / 100, 2) if plan.gst else 0.0
            total_amount = round(float(plan.price) + gst_amount, 2)
            Invoice.objects.create(
                customer=customer,
                center=center,
                plan=plan,
                amount=total_amount,
                date=customer.start_date,
                status='pending',
            )
        return customer


class StrictBooleanField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if data is True or data is False:
            return data
        raise serializers.ValidationError("gst must be true or false only.")


class PlanSerializer(serializers.ModelSerializer):
    gst = StrictBooleanField()
    gst_amount = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'plan_name', 'description', 'duration_months', 'price', 'gst', 'gst_amount', 'total_amount', 'status']
        read_only_fields = ['gst_amount', 'total_amount']

    def get_gst_amount(self, obj):
        if obj.gst:
            return round(float(obj.price) * 18 / 100, 2)
        return 0.0

    def get_total_amount(self, obj):
        if obj.gst:
            return round(float(obj.price) + float(obj.price) * 18 / 100, 2)
        return float(obj.price)

    def validate_plan_name(self, value):
        qs = Plan.objects.filter(plan_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A plan with this name already exists.")
        return value


class CenterSerializer(serializers.ModelSerializer):
    total_customers = serializers.SerializerMethodField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Center
        fields = ['id', 'center_name', 'location', 'mobile', 'email', 'password', 'poc_name', 'poc_contact', 'status', 'created_at', 'total_customers']
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

    def validate_email(self, value):
        qs = Center.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A center with this email already exists.")
        if not self.instance and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already used by another user.")
        return value

    def validate(self, attrs):
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({"password": "Password is required when creating a center."})
        return attrs

    def validate_status(self, value):
        if value not in ('active', 'inactive'):
            raise serializers.ValidationError("Status must be 'active' or 'inactive'.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        center = Center.objects.create(**validated_data)
        # Auto-create branch user
        username = validated_data['email'].split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=password,
            role='branch_user',
            center=center,
            is_active=True,
        )
        return center

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email_changed = 'email' in validated_data and validated_data['email'] != instance.email
        old_email = instance.email
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Get or create branch user
        from .models import User
        branch_user = User.objects.filter(center=instance, role='branch_user').first()
        
        if not branch_user:
            # Create branch user if it doesn't exist
            username = instance.email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            branch_user = User.objects.create_user(
                username=username,
                email=instance.email,
                password=password or 'center123',  # Default password if not provided
                role='branch_user',
                center=instance,
                is_active=True,
            )
        else:
            # Update existing branch user
            if email_changed:
                branch_user.email = instance.email
                # Also update username to match new email
                new_username = instance.email.split('@')[0]
                base_username = new_username
                counter = 1
                while User.objects.filter(username=new_username).exclude(pk=branch_user.pk).exists():
                    new_username = f"{base_username}{counter}"
                    counter += 1
                branch_user.username = new_username
            if password:
                branch_user.set_password(password)
            if email_changed or password:
                branch_user.save()
        
        return instance


class CenterMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id', 'center_name']


class SlotSerializer(serializers.ModelSerializer):
    slot_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    available_count = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'slot_time', 'total_slot', 'available_count', 'status', 'is_enabled', 'created_at']
        read_only_fields = ['id', 'created_at', 'slot_time', 'status', 'available_count']

    def get_slot_time(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"

    def get_status(self, obj):
        return 'enabled' if obj.is_enabled else 'disabled'

    def get_available_count(self, obj):
        request = self.context.get('request')
        booking_date = request.query_params.get('date') if request else None
        center = request.query_params.get('center') if request else None
        
        if booking_date:
            booking_filter = {'slot': obj, 'booking_date': booking_date}
            if center:
                booking_filter['center_id'] = center
            booked = SlotBooking.objects.filter(**booking_filter).count()
        else:
            booked = 0
        return max(obj.total_slot - booked, 0)

    def validate(self, attrs):
        if attrs.get("start_time") and attrs.get("end_time") and attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError("End time must be greater than start time.")
        return attrs


class SlotBookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    slot_time = serializers.SerializerMethodField()
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False
    )
    slot_id = serializers.PrimaryKeyRelatedField(
        queryset=Slot.objects.all(), source='slot', write_only=True, required=False
    )
    center_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = SlotBooking
        fields = ['id', 'customer', 'customer_id', 'customer_name', 'slot', 'slot_id', 'slot_time', 'center_id', 'booking_date', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'customer_name', 'slot_time']
        extra_kwargs = {
            'customer': {'required': False},
            'slot': {'required': False},
        }

    def get_slot_time(self, obj):
        return f"{obj.slot.start_time.strftime('%I:%M %p')} - {obj.slot.end_time.strftime('%I:%M %p')}"

    def validate(self, attrs):
        slot = attrs.get('slot')
        booking_date = attrs.get('booking_date')
        customer = attrs.get('customer')
        center_id = attrs.get('center_id')

        if not slot:
            raise serializers.ValidationError({'slot': 'This field is required.'})
        if not customer:
            raise serializers.ValidationError({'customer': 'This field is required.'})

        if not slot.is_enabled:
            raise serializers.ValidationError({'slot': 'This slot is disabled.'})

        # Check if slot is full for this center on this date
        booking_filter = {'slot': slot, 'booking_date': booking_date}
        if center_id:
            booking_filter['center_id'] = center_id
        
        booked_count_for_date = SlotBooking.objects.filter(**booking_filter).count()
        if booked_count_for_date >= slot.total_slot:
            raise serializers.ValidationError({'slot': 'This slot is already full for the selected date at this center.'})

        # Check if customer already booked this slot on this date
        if SlotBooking.objects.filter(
            customer=customer, slot=slot, booking_date=booking_date
        ).exists():
            raise serializers.ValidationError({'non_field_errors': 'This customer already booked this slot for this date.'})
        return attrs

    def create(self, validated_data):
        center_id = validated_data.pop('center_id', None)
        booking = SlotBooking.objects.create(**validated_data)
        if center_id:
            booking.center_id = center_id
            booking.save()
        return booking


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_id = serializers.CharField(read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    center_name = serializers.CharField(source='center.center_name', read_only=True)
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)
    download_invoice_url = serializers.SerializerMethodField()
    gst_applied = serializers.SerializerMethodField()
    gst_amount = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_id',
            'customer', 'customer_name',
            'center', 'center_name',
            'plan', 'plan_name',
            'amount', 'gst_applied', 'gst_amount', 'subtotal',
            'date', 'status', 'created_at', 'download_invoice_url'
        ]
        read_only_fields = ['id', 'invoice_id', 'created_at', 'customer_name', 'center_name', 'plan_name', 'download_invoice_url', 'gst_applied', 'gst_amount', 'subtotal']

    def get_download_invoice_url(self, obj):
        return f'/api/invoices/{obj.id}/download/excel/'

    def get_gst_applied(self, obj):
        return obj.plan.gst if obj.plan else False

    def get_gst_amount(self, obj):
        if obj.plan and obj.plan.gst:
            return round(float(obj.amount) * 18 / 100, 2)
        return 0.0

    def get_subtotal(self, obj):
        gst_amount = self.get_gst_amount(obj)
        return round(float(obj.amount) + gst_amount, 2)

    def validate(self, attrs):
        customer = attrs.get('customer')
        center = attrs.get('center')
        if customer and center and customer.center and customer.center != center:
            raise serializers.ValidationError({
                'center': f"Center must match the customer's center (ID: {customer.center.id} - {customer.center.center_name})."
            })
        return attrs
