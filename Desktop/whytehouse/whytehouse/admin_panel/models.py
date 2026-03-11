from django.db import models
from datetime import time
from django.utils import timezone
from django.utils.text import slugify

# BLOG CATEGORY MODEL
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Blog Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# LEAD MODEL
class Lead(models.Model):
    SOURCE_CHOICES = (
        ('Direct', 'Direct Contact'),
        ('Website', 'Website'),
        ('Manual', 'Manual Entry'),
        ('Referral', 'Referral'),
        ('Enquire Now', 'Enquire Now'),
    )
    ENQUIRY_TYPE_CHOICES = (
        ('General', 'General Enquiry'),
        ('International', 'International'),
        ('Domestic', 'Domestic'),
    )
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Junk', 'Junk'),
    )
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    place = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Manual')
    enquiry_type = models.CharField(max_length=50, choices=ENQUIRY_TYPE_CHOICES, default='General')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    is_viewed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('hotel', 'Luxury Hotel'),
        ('resort', 'Mountain Resort'),
        ('beach', 'Beach Resort'),
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
    ]

    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    address = models.TextField()
    summary = models.TextField()
    owner_name = models.CharField(max_length=150, blank=True, null=True)
    owner_contact = models.CharField(max_length=20, blank=True, null=True)

    # comma separated amenities (TEXT)
    amenities = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def amenity_list(self):
        if self.amenities:
            return [a.strip() for a in self.amenities.split(",") if a.strip()]
        return []

class Destination(models.Model):
    CATEGORY_CHOICES = (
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    )
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Domestic')
    description = models.TextField(blank=True, null=True)
    packages_start_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    map_image = models.ImageField(upload_to='destinations/maps/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['-created_at']

# TRAVEL PACKAGE MODEL
class TravelPackage(models.Model):
    CATEGORY_CHOICES = (
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    )

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages"
    )

    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='travel_packages/', blank=True, null=True)
    active = models.BooleanField(default=True)
    itinerary = models.TextField(blank=True, null=True)
    inclusions = models.TextField(blank=True, null=True)
    exclusions = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    story_main_image = models.ImageField(upload_to='package_stories/', blank=True, null=True)
    story_side_image1 = models.ImageField(upload_to='package_stories/', blank=True, null=True)
    story_side_image2 = models.ImageField(upload_to='package_stories/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Junk', 'Junk'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries"
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


#EMPLOYEE MODEL OF ADMINAPP

class Employee(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('On Leave', 'On Leave'),
    )
    
    # Basic Information
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    join_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    profile_picture = models.ImageField(upload_to='employee/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        ordering = ['-created_at']

        
# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('checking', 'Checking'),
    ]
    
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='current'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account_name} - {self.account_number}"
    
    class Meta:
        ordering = ['-created_at']


class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Corporate', 'Corporate'),
        ('Government', 'Government'),
    ]
    
    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
    ]
    
    customer_type = models.CharField(
        max_length=50,
        choices=CUSTOMER_TYPE_CHOICES,
        default='Individual'
    )
    salutation = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, unique=True)
    same_as_whatsapp = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    work_number = models.CharField(max_length=20, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.display_name} - {self.contact_number}"
    
    class Meta:
        ordering = ['-created_at']


class Resort(models.Model):
    RESORT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    resort_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=RESORT_STATUS_CHOICES,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.resort_name
    
    class Meta:
        ordering = ['-created_at']


class Meal(models.Model):
    MEAL_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    included_meals = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=MEAL_STATUS_CHOICES,
        default='Available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class Voucher(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    voucher_no = models.CharField(max_length=50, unique=True)
    voucher_date = models.DateField(null=True, blank=True)

    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    resort = models.ForeignKey(Resort, on_delete=models.SET_NULL, null=True, blank=True)

    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)

    # ✅ stop migration prompts
    checkin_time = models.TimeField(default=time(0, 0))
    checkout_time = models.TimeField(default=time(0, 0))

    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    nights = models.IntegerField(default=1)

    # ✅ safer (avoid non-null issues)
    pax_notes = models.TextField(blank=True, default="")

    room_type = models.CharField(max_length=100, blank=True, default="")
    no_of_rooms = models.IntegerField(default=1)

    meals_plan = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True)
    bank_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    resort_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    from_whytehouse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    note_for_resort = models.TextField(max_length=130, blank=True, default="")
    note_for_guest = models.TextField(max_length=130, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.voucher_no} - {self.customer.display_name if self.customer else 'N/A'}"

    class Meta:
        ordering = ['-created_at']


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    resort = models.ForeignKey(Resort, on_delete=models.SET_NULL, null=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    pax_total = models.IntegerField(default=0)
    pax_notes = models.TextField(blank=True, null=True)
    nights = models.IntegerField(default=1)
    room_type = models.CharField(max_length=100, blank=True)
    rooms = models.IntegerField(default=1)
    meals_plan = models.CharField(max_length=50, blank=True)
    bank_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    resort_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_no} - {self.customer.display_name}"
    
    class Meta:
        ordering = ['-created_at']

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]
    
    CATEGORY_CHOICES = [
        ('travel', 'Travel'),
        ('adventure', 'Adventure'),
        ('culture', 'Culture'),
        ('food', 'Food'),
        ('tips', 'Tips'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    package_id = models.CharField(max_length=50, blank=True, null=True)
    
    author_name = models.CharField(max_length=100)
    author_summary = models.TextField(max_length=500)
    reading_time = models.PositiveIntegerField(default=1)
    publish_date = models.DateField()
    
    # Main images
    featured_image = models.ImageField(upload_to='blog_images/featured/', blank=True, null=True)
    featured_image_url = models.URLField(blank=True, null=True)
    
    hashtags = models.CharField(max_length=500, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        return self.featured_image.url if self.featured_image else self.featured_image_url


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/content/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image {self.order + 1} for {self.blog.title}"


from django.db import models

class Feedback(models.Model):

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    FEEDBACK_TYPE_CHOICES = [
        ('Travel Package', 'Travel Package'),
        ('Customer Service', 'Customer Service'),
        ('Booking Experience', 'Booking Experience'),
        ('Property Management', 'Property Management'),
        ('Website Experience', 'Website Experience'),
        ('Trip Management', 'Trip Management'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10, blank=True)

    feedback_type = models.CharField(
        max_length=50,
        choices=FEEDBACK_TYPE_CHOICES,
        default='Other'
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"


class FeedbackImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='feedback_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.feedback.name}"