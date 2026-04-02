from django.db import models

class Customer(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    ]

    WAVE_CHOICES = [
        ('Wave A', 'Wave A'),
        ('Wave B', 'Wave B'),
        ('Wave C', 'Wave C'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expiring', 'Expiring'),
        ('Expired', 'Expired'),
    ]

    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    wave = models.CharField(max_length=20, choices=WAVE_CHOICES)

    days_left = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.days_left <= 0:
            self.status = 'Expired'
        elif self.days_left <= 5:
            self.status = 'Expiring'
        else:
            self.status = 'Active'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name