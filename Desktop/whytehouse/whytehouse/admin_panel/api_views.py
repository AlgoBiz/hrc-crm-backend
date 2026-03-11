from django.db.models import Q, Sum
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Blog,
    BlogCategory,
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
    Invoice,Feedback,
)
from .serializers import (
    BlogSerializer,
    BlogListSerializer,
    BlogCategorySerializer,
    LeadSerializer,
    PropertySerializer,
    TravelPackageSerializer,
    TravelPackageListSerializer,
    DestinationSerializer,
    CustomerSerializer,
    MealSerializer,
    AccountSerializer,
    InquirySerializer,
    EmployeeSerializer,
    ResortSerializer,
    VoucherSerializer,
    InvoiceSerializer,
    FeedbackSerializer,
)

# ==================== BLOG CATEGORY VIEWSET ====================
class BlogCategoryViewSet(viewsets.ModelViewSet):

    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all().order_by('order', 'name')

    def get_queryset(self):
        qs = super().get_queryset()

        is_active = (self.request.query_params.get("is_active") or "").strip().lower()
        if is_active == "true":
            qs = qs.filter(is_active=True)
        elif is_active == "false":
            qs = qs.filter(is_active=False)

        search_query = (self.request.query_params.get("search") or "").strip()
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query) |
                Q(slug__icontains=search_query)
            )

        return qs

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Get all active categories"""
        categories = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def blogs(self, request, pk=None):
        """Get all blogs for a specific category"""
        category = self.get_object()
        blogs = Blog.objects.filter(status="published", category=category.slug).order_by("-publish_date")
        serializer = BlogListSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data)


# ==================== BLOG VIEWSET ====================
class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Blogs
    Filters: search, status, category
    """
    queryset = Blog.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return BlogListSerializer
        return BlogSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        search_query = (self.request.query_params.get("search") or "").strip()
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(author_name__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        category_filter = (self.request.query_params.get("category") or "").strip()
        if category_filter:
            qs = qs.filter(category=category_filter)

        return qs

    def perform_create(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=hashtags_value or serializer.validated_data.get("tags", "")
        )

    def perform_update(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=hashtags_value or serializer.validated_data.get("tags", "")
        )

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "published_count": qs.filter(status="published").count(),
            "draft_count": qs.filter(status="draft").count(),
            "total": qs.count(),
        })

    @action(detail=False, methods=["get"])
    def published(self, request):
        """Get all published blogs"""
        blogs = self.get_queryset().filter(status="published").order_by("-publish_date")
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get blogs grouped by category"""
        categories = BlogCategory.objects.filter(is_active=True).order_by('order', 'name')
        result = {}
        for cat in categories:
            blogs = Blog.objects.filter(status="published", category=cat.slug).order_by("-publish_date")[:6]
            result[cat.slug] = BlogListSerializer(blogs, many=True, context={"request": request}).data
        return Response(result)


# ==================== LEAD VIEWSET ====================
class LeadViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Leads
    Filters: type, source, new, search
    """
    serializer_class = LeadSerializer
    queryset = Lead.objects.all().order_by("-created_at")

    def get_queryset(self):
        qs = super().get_queryset()

        enquiry_type = (self.request.query_params.get("type") or "").strip()
        source_filter = (self.request.query_params.get("source") or "").strip()
        new_leads = (self.request.query_params.get("new") or "").strip().lower()
        search_query = (self.request.query_params.get("search") or "").strip()

        if enquiry_type:
            qs = qs.filter(enquiry_type=enquiry_type)

        if source_filter:
            qs = qs.filter(source=source_filter)

        if new_leads == "true":
            qs = qs.filter(source="Enquire Now")

        if search_query:
            qs = qs.filter(
                Q(full_name__icontains=search_query) |
                Q(mobile_number__icontains=search_query) |
                Q(place__icontains=search_query) |
                Q(remarks__icontains=search_query)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        return Response({
            "general_count": Lead.objects.filter(enquiry_type="General").count(),
            "international_count": Lead.objects.filter(enquiry_type="International").count(),
            "domestic_count": Lead.objects.filter(enquiry_type="Domestic").count(),
            "new_leads_count": Lead.objects.filter(source="Enquire Now").count(),
            "total": Lead.objects.count(),
        })


# ==================== PROPERTY VIEWSET ====================
class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Properties
    Filters: property_type, location, search
    """
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        ptype = (self.request.query_params.get("property_type") or "").strip()
        location = (self.request.query_params.get("location") or "").strip()
        search = (self.request.query_params.get("search") or "").strip()

        if ptype:
            qs = qs.filter(property_type=ptype)

        if location:
            qs = qs.filter(location__icontains=location)

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(location__icontains=search)
                | Q(address__icontains=search)
                | Q(summary__icontains=search)
                | Q(owner_name__icontains=search)
                | Q(owner_contact__icontains=search)
                | Q(amenities__icontains=search)
            )

        return qs


# ==================== DESTINATION VIEWSET ====================
class DestinationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Destinations
    Filters: category, is_popular, search
    """
    queryset = Destination.objects.all().order_by("-created_at")
    serializer_class = DestinationSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        category = (self.request.query_params.get("category") or "").strip()
        if category:
            qs = qs.filter(category=category)

        is_popular = (self.request.query_params.get("is_popular") or "").strip().lower()
        if is_popular == "true":
            qs = qs.filter(is_popular=True)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(country__icontains=search)
                | Q(description__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "domestic_count": qs.filter(category="Domestic").count(),
            "international_count": qs.filter(category="International").count(),
            "popular_count": qs.filter(is_popular=True).count(),
        })

    @action(detail=True, methods=["get"])
    def packages(self, request, pk=None):
        destination = self.get_object()
        packages = destination.packages.filter(active=True)
        serializer = TravelPackageListSerializer(
            packages, many=True, context={"request": request}
        )
        return Response(serializer.data)


# ==================== TRAVEL PACKAGE VIEWSET ====================
class TravelPackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Travel Packages
    Filters: category, active, destination, country, min_price, max_price, search
    """
    queryset = TravelPackage.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return TravelPackageListSerializer
        return TravelPackageSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        category = (self.request.query_params.get("category") or "").strip()
        if category:
            qs = qs.filter(category=category)

        active = (self.request.query_params.get("active") or "").strip().lower()
        if active == "true":
            qs = qs.filter(active=True)
        elif active == "false":
            qs = qs.filter(active=False)

        destination_id = (self.request.query_params.get("destination") or "").strip()
        if destination_id:
            qs = qs.filter(destination_id=destination_id)

        country = (self.request.query_params.get("country") or "").strip()
        if country:
            qs = qs.filter(country__icontains=country)

        min_price = (self.request.query_params.get("min_price") or "").strip()
        max_price = (self.request.query_params.get("max_price") or "").strip()
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(location__icontains=search)
                | Q(country__icontains=search)
                | Q(description__icontains=search)
                | Q(itinerary__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(active=True).count(),
            "inactive_count": qs.filter(active=False).count(),
            "domestic_count": qs.filter(category="Domestic").count(),
            "international_count": qs.filter(category="International").count(),
        })

    @action(detail=False, methods=["get"])
    def featured(self, request):
        packages = self.get_queryset().filter(active=True)[:6]
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        domestic = self.get_queryset().filter(category="Domestic", active=True)[:6]
        international = self.get_queryset().filter(category="International", active=True)[:6]
        
        return Response({
            "domestic": TravelPackageListSerializer(
                domestic, many=True, context={"request": request}
            ).data,
            "international": TravelPackageListSerializer(
                international, many=True, context={"request": request}
            ).data,
        })


# ==================== CUSTOMER VIEWSET ====================
class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Customers
    Filters: customer_type, search
    """
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        customer_type = (self.request.query_params.get("customer_type") or "").strip()
        if customer_type:
            qs = qs.filter(customer_type=customer_type)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(display_name__icontains=search)
                | Q(contact_number__icontains=search)
                | Q(place__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "individual_count": qs.filter(customer_type="Individual").count(),
            "corporate_count": qs.filter(customer_type="Corporate").count(),
            "government_count": qs.filter(customer_type="Government").count(),
        })


# ==================== MEAL VIEWSET ====================
class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Meals
    Filters: status, search
    """
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "available_count": qs.filter(status="Available").count(),
            "unavailable_count": qs.filter(status="Unavailable").count(),
        })


# ==================== ACCOUNT VIEWSET ====================
class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Accounts
    Filters: account_type, search
    """
    queryset = Account.objects.all().order_by("-created_at")
    serializer_class = AccountSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        account_type = (self.request.query_params.get("account_type") or "").strip()
        if account_type:
            qs = qs.filter(account_type=account_type)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(account_name__icontains=search)
                | Q(bank_name__icontains=search)
                | Q(account_number__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
        })


# ==================== INQUIRY VIEWSET ====================
class InquiryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Inquiries
    Filters: status, search
    """
    queryset = Inquiry.objects.all().order_by("-created_at")
    serializer_class = InquirySerializer

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(package__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "new_count": qs.filter(status="New").count(),
            "contacted_count": qs.filter(status="Contacted").count(),
            "converted_count": qs.filter(status="Converted").count(),
            "junk_count": qs.filter(status="Junk").count(),
        })


# ==================== EMPLOYEE VIEWSET ====================
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Employees
    Filters: status, role, search
    """
    queryset = Employee.objects.all().order_by("-created_at")
    serializer_class = EmployeeSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        role = (self.request.query_params.get("role") or "").strip()
        if role:
            qs = qs.filter(role__icontains=role)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(role__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(status="Active").count(),
            "inactive_count": qs.filter(status="Inactive").count(),
        })


# ==================== RESORT VIEWSET ====================
class ResortViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Resorts
    Filters: status, location, search
    """
    queryset = Resort.objects.all().order_by("-created_at")
    serializer_class = ResortSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        location = (self.request.query_params.get("location") or "").strip()
        if location:
            qs = qs.filter(location__icontains=location)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(resort_name__icontains=search)
                | Q(location__icontains=search)
                | Q(contact_person__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(status="Active").count(),
            "inactive_count": qs.filter(status="Inactive").count(),
        })


# ==================== VOUCHER VIEWSET ====================
class VoucherViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Vouchers
    Filters: customer, resort, check_in_date, check_out_date, search
    """
    queryset = Voucher.objects.all().order_by("-created_at")
    serializer_class = VoucherSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        customer_id = (self.request.query_params.get("customer") or "").strip()
        if customer_id:
            qs = qs.filter(customer_id=customer_id)

        resort_id = (self.request.query_params.get("resort") or "").strip()
        if resort_id:
            qs = qs.filter(resort_id=resort_id)

        check_in = (self.request.query_params.get("checkin_date") or "").strip()
        if check_in:
            qs = qs.filter(checkin_date__gte=check_in)

        check_out = (self.request.query_params.get("checkout_date") or "").strip()
        if check_out:
            qs = qs.filter(checkout_date__lte=check_out)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(voucher_no__icontains=search)
                | Q(customer__display_name__icontains=search)
                | Q(resort__resort_name__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        total_amount = qs.aggregate(total=Sum('total_amount'))['total'] or 0
        return Response({
            "total": qs.count(),
            "total_amount": float(total_amount),
        })


# ==================== INVOICE VIEWSET ====================
class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Invoices
    Filters: customer, resort, sales_person, payment_mode, date_from, date_to, search
    """
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        customer_id = (self.request.query_params.get("customer") or "").strip()
        if customer_id:
            qs = qs.filter(customer_id=customer_id)

        resort_id = (self.request.query_params.get("resort") or "").strip()
        if resort_id:
            qs = qs.filter(resort_id=resort_id)

        sales_person_id = (self.request.query_params.get("sales_person") or "").strip()
        if sales_person_id:
            qs = qs.filter(sales_person_id=sales_person_id)

        # invoice model has no payment_mode field
        date_from = (self.request.query_params.get("date_from") or "").strip()
        if date_from:
            qs = qs.filter(created_at__gte=date_from)

        date_to = (self.request.query_params.get("date_to") or "").strip()
        if date_to:
            qs = qs.filter(created_at__lte=date_to)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(invoice_no__icontains=search)
                | Q(customer__display_name__icontains=search)
                | Q(resort__resort_name__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        total_val = qs.aggregate(total=Sum('total'))['total'] or 0
        paid_val = qs.aggregate(total=Sum('received'))['total'] or 0
        pending_val = qs.aggregate(total=Sum('pending'))['total'] or 0
        
        return Response({
            "total": qs.count(),
            "total_amount": float(total_val),
            "received_amount": float(paid_val),
            "pending_amount": float(pending_val),
        })

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """Get invoices with pending amount"""
        invoices = self.get_queryset().filter(pending__gt=0)
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)




class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all().prefetch_related('images').order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve", "featured"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        feedback_type = (self.request.query_params.get("feedback_type") or "").strip()
        if feedback_type:
            qs = qs.filter(feedback_type=feedback_type)
        return qs

    @action(detail=False, methods=["get"], url_path="featured", permission_classes=[permissions.AllowAny])
    def featured(self, request):
        qs = Feedback.objects.filter(featured=True).prefetch_related('images').order_by("-created_at")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)