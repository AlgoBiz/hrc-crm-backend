from rest_framework import serializers

from .models import (
    Blog,
    BlogCategory,
    BlogImage,
    Lead,
    Property,
    TravelPackage,
    Destination,
    Customer,
    Meal,
    Account,
    Inquiry,
    Employee,
    Resort,
    Voucher,
    Invoice,
    Feedback,
)


# ==================== BLOG CATEGORY SERIALIZER ====================
class BlogCategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = [
            "id",
            "name",
            "slug",
            "order",
            "is_active",
            "created_at",
            "blog_count",
        ]
        read_only_fields = ["id", "created_at", "blog_count"]

    def get_blog_count(self, obj):
        return Blog.objects.filter(status="published", category=obj.slug).count()


# ==================== BLOG IMAGE SERIALIZER ====================
class BlogImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogImage
        fields = ["id", "image", "image_url", "order", "tag"]
        read_only_fields = ["id", "image_url", "tag"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== BLOG SERIALIZER ====================

class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    content_images = BlogImageSerializer(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "status",
            "category",
            "category_name",
            "package_id",
            "author_name",
            "author_summary",
            "reading_time",
            "publish_date",
            "featured_image",
            "featured_image_url",
            "image_url",
            "hashtags",
            "tags",
            "tag_list",
            "content_images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url", "category_name", "tag_list", "content_images"]

    def get_image_url(self, obj):
        return obj.image_url

    def get_category_name(self, obj):
        if obj.category:
            cat = BlogCategory.objects.filter(slug=obj.category).first()
            return cat.name if cat else obj.category
        return None

    def get_tag_list(self, obj):
        raw = obj.tags or obj.hashtags or ""
        return [t.strip() for t in str(raw).split(",") if t.strip()]


class BlogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog list views"""
    image_url = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "status",
            "category",
            "category_name",
            "author_name",
            "reading_time",
            "publish_date",
            "image_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "image_url", "category_name"]

    def get_image_url(self, obj):
        return obj.image_url

    def get_category_name(self, obj):
        if obj.category:
            cat = BlogCategory.objects.filter(slug=obj.category).first()
            return cat.name if cat else obj.category
        return None


# ==================== LEAD SERIALIZER ====================
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "mobile_number",
            "place",
            "source",
            "enquiry_type",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== PROPERTY SERIALIZER ====================
class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    amenity_list = serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "property_type",
            "location",
            "website",
            "address",
            "summary",
            "owner_name",
            "owner_contact",
            "amenities",
            "amenity_list",
            "image",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== DESTINATION SERIALIZER ====================
class DestinationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    package_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "country",
            "category",
            "description",
            "image",
            "image_url",
            "is_popular",
            "created_at",
            "package_count",
        ]
        read_only_fields = ["id", "created_at", "image_url", "package_count"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_package_count(self, obj):
        return obj.packages.filter(active=True).count()


# ==================== TRAVEL PACKAGE SERIALIZERS ====================
class TravelPackageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    story_main_image_url = serializers.SerializerMethodField()
    story_side_image1_url = serializers.SerializerMethodField()
    story_side_image2_url = serializers.SerializerMethodField()
    destination_details = DestinationSerializer(source='destination', read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "name",
            "category",
            "destination",
            "destination_details",
            "location",
            "country",
            "price",
            "duration",
            "description",
            "image",
            "image_url",
            "active",
            "itinerary",
            "inclusions",
            "exclusions",
            "meta_title",
            "meta_description",
            "story_main_image",
            "story_main_image_url",
            "story_side_image1",
            "story_side_image1_url",
            "story_side_image2",
            "story_side_image2_url",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "image_url",
            "story_main_image_url",
            "story_side_image1_url",
            "story_side_image2_url",
            "destination_details",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_story_main_image_url(self, obj):
        request = self.context.get("request")
        if obj.story_main_image and request:
            return request.build_absolute_uri(obj.story_main_image.url)
        return None

    def get_story_side_image1_url(self, obj):
        request = self.context.get("request")
        if obj.story_side_image1 and request:
            return request.build_absolute_uri(obj.story_side_image1.url)
        return None

    def get_story_side_image2_url(self, obj):
        request = self.context.get("request")
        if obj.story_side_image2 and request:
            return request.build_absolute_uri(obj.story_side_image2.url)
        return None


class TravelPackageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    image_url = serializers.SerializerMethodField()
    destination_name = serializers.CharField(source='destination.name', read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "name",
            "category",
            "destination_name",
            "location",
            "country",
            "price",
            "duration",
            "image",
            "image_url",
            "active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "image_url", "destination_name"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== CUSTOMER SERIALIZER ====================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "customer_type",
            "salutation",
            "first_name",
            "last_name",
            "display_name",
            "place",
            "contact_number",
            "same_as_whatsapp",
            "whatsapp_number",
            "work_number",
            "gst_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== MEAL SERIALIZER ====================
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "id",
            "meal_plan",
            "description",
            "price_per_person",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== ACCOUNT SERIALIZER ====================
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_name",
            "account_type",
            "bank_name",
            "branch",
            "account_number",
            "ifsc_code",
            "balance",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== INQUIRY SERIALIZER ====================
class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "package",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== EMPLOYEE SERIALIZER ====================
class EmployeeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "role",
            "email",
            "phone",
            "address",
            "date_of_joining",
            "salary",
            "status",
            "image",
            "image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== RESORT SERIALIZER ====================
class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = [
            "id",
            "resort_name",
            "location",
            "contact_person",
            "contact_number",
            "email",
            "price_per_night",
            "amenities",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== VOUCHER SERIALIZER ====================
class VoucherSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.display_name', read_only=True)
    resort_name = serializers.CharField(source='resort.resort_name', read_only=True)
    meal_plan_name = serializers.CharField(source='meal.meal_plan', read_only=True)

    class Meta:
        model = Voucher
        fields = [
            "id",
            "customer",
            "customer_name",
            "voucher_no",
            "resort",
            "resort_name",
            "check_in_date",
            "check_out_date",
            "number_of_nights",
            "number_of_adults",
            "number_of_children",
            "meal",
            "meal_plan_name",
            "room_type",
            "special_requests",
            "total_amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "customer_name", "resort_name", "meal_plan_name"]


# ==================== INVOICE SERIALIZER ====================
class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.display_name', read_only=True)
    resort_name = serializers.CharField(source='resort.resort_name', read_only=True)
    meal_plan_name = serializers.CharField(source='meal.meal_plan', read_only=True)
    account_name = serializers.CharField(source='account.account_name', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer",
            "customer_name",
            "invoice_no",
            "resort",
            "resort_name",
            "check_in_date",
            "check_out_date",
            "number_of_nights",
            "number_of_adults",
            "number_of_children",
            "meal",
            "meal_plan_name",
            "room_type",
            "room_rate",
            "meal_cost",
            "other_charges",
            "discount",
            "total_amount",
            "paid_amount",
            "pending_amount",
            "payment_mode",
            "account",
            "account_name",
            "sales_person",
            "sales_person_name",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "customer_name",
            "resort_name",
            "meal_plan_name",
            "account_name",
            "sales_person_name",
        ]
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "id",
            "name",
            "email",
            "mobile_number",
            "rating",
            "feedback",
            "featured",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]