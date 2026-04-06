from rest_framework import serializers

from .models import Customer, User, Center, Plan, Slot, SlotBooking, Invoice
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'mobile',
            'email',
            'center',
            'plan',
            'wave',
            'start_date',
            'expiry_date',
            'last_visit',
            'status',
            'address',
            'city',
            'state',
            'pincode',
            'occupation',
            'dob',
            'created_at',
        ]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")

        attrs["user"] = user
        return attrs


    password = serializers.CharField(write_only=True)
    center_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role', 'center_id']

    def create(self, validated_data):
        center_id = validated_data.pop('center_id', None)
        center = Center.objects.get(id=center_id) if center_id else None
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            center=center,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'mobile',
            'email',
            'center',
            'plan',
            'wave',
            'start_date',
            'expiry_date',
            'last_visit',
            'status',
            'address',
            'city',
            'state',
            'pincode',
            'occupation',
            'dob',
            'created_at',
        ]

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 
            'plan_name',
            'description',
            'duration_months', 
            'price', 
            'status'
            ]


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = [
            'id',
            'center_name',
            'location',
            'mobile',
            'status',
        ]

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = [
            "id",
            "center_name",
            "location",
            "mobile",
            "email",
            "poc_name",
            "poc_contact",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
class SlotSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source="center.center_name", read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = [
            "id",
            "center",
            "center_name",
            "start_time",
            "end_time",
            "slot_time",
            "booked_count",
            "total_slot",
            "status",
            "is_enabled",
            "created_at",
        ]
        read_only_fields = ["id", "booked_count", "created_at", "slot_time", "center_name"]

    def get_slot_time(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be greater than start time.")
        return attrs

class SlotBookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = [
            "id",
            "customer",
            "customer_name",
            "slot",
            "slot_time",
            "booking_date",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "customer_name", "slot_time"]

    def get_slot_time(self, obj):
        return f"{obj.slot.start_time.strftime('%I:%M %p')} - {obj.slot.end_time.strftime('%I:%M %p')}"

    def validate(self, attrs):
        slot = attrs.get("slot")
        customer = attrs.get("customer")
        booking_date = attrs.get("booking_date")

        if not slot.is_enabled:
            raise serializers.ValidationError({"slot": "This slot is disabled."})

        if slot.booked_count >= slot.total_slot:
            raise serializers.ValidationError({"slot": "This slot is already full."})

        if SlotBooking.objects.filter(
            customer=customer,
            slot=slot,
            booking_date=booking_date
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": "This customer already booked this slot for this date."}
            )

        return attrs

    def create(self, validated_data):
        slot = validated_data["slot"]

        booking = SlotBooking.objects.create(**validated_data)

        slot.booked_count += 1
        slot.save()

        return booking
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'customer',
            'plan',
            'amount',
            'date',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
