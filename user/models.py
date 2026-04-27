from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Center(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    center_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    poc_name = models.CharField(max_length=100, blank=True, null=True)
    poc_contact = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.center_name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('branch_user', 'Branch User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='branch_user')
    center = models.ForeignKey('Center', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.username


class Wave(models.Model):
    wave_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wave_name



class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
    ]
    WAVE_CHOICES = [
        ('Vikas', 'Vikas'),
        ('Amrith', 'Amrith'),
        ('Samriddhi', 'Samriddhi'),
        ('Zayana', 'Zayana'),
        ('Prabhav', 'Prabhav'),
        ('Sexellence', 'Sexellence'),
        ('Aanandha', 'Aanandha'),
        ('Relax', 'Relax'),
    ]
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=45, blank=True, null=True)
    center = models.ForeignKey('Center', on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    wave = models.CharField(max_length=20, choices=WAVE_CHOICES, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    last_visit = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_computed_status(self):
        from datetime import date
        if not self.expiry_date:
            return self.status
        today = date.today()
        days_left = (self.expiry_date - today).days
        if days_left < 0:
            return 'expired'
        elif days_left <= 10:
            return 'expiring'
        return 'active'

    def save(self, *args, **kwargs):
        self.status = self.get_computed_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plan(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    plan_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_months = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.plan_name
    

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='invoices')
    center = models.ForeignKey('Center', on_delete=models.CASCADE, related_name='invoices')
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def invoice_id(self):
        return f"INV-{self.id:03d}"

    def __str__(self):
        return self.invoice_id

class Slot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked_count = models.IntegerField(default=0)
    total_slot = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class SlotBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='slot_bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='slot_bookings')
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='slot_bookings', null=True, blank=True)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.slot}"