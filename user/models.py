from django.db import models
from django.contrib.auth.models import AbstractUser

class Center(models.Model):
    center_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    poc_name = models.CharField(max_length=100, blank=True, null=True)
    poc_contact = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.center_name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('branch_user', 'Branch User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    center = models.ForeignKey('Center', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.username



class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
    ]
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=45, blank=True, null=True)
    center = models.ForeignKey('Center', on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.CharField(max_length=100)
    wave = models.CharField(max_length=20)
    start_date = models.DateField()
    expiry_date = models.DateField()
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
    def __str__(self):
        return self.name


class Plan(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    plan_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_months = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

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

    invoice_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='invoices')
    center = models.ForeignKey('Center', on_delete=models.CASCADE, related_name='invoices')
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_path = models.FileField(upload_to='invoices/', blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

class Slot(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked_count = models.IntegerField(default=0)
    total_slot = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Enabled')
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class SlotBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='slot_bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='slot_bookings')
    booking_date = models.DateField()
    status = models.CharField(max_length=20, default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.slot}"