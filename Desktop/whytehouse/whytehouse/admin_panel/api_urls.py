from rest_framework.routers import DefaultRouter
from .api_views import (
    BlogViewSet,
    BlogCategoryViewSet,
    LeadViewSet,
    PropertyViewSet,
    TravelPackageViewSet,
    DestinationViewSet,
    CustomerViewSet,
    MealViewSet,
    AccountViewSet,
    InquiryViewSet,
    EmployeeViewSet,
    ResortViewSet,
    VoucherViewSet,
    InvoiceViewSet,
    FeedbackViewSet,
)

router = DefaultRouter()

# Core APIs
router.register(r"blogs", BlogViewSet, basename="blogs")
router.register(r"blog-categories", BlogCategoryViewSet, basename="blog-categories")
router.register(r"leads", LeadViewSet, basename="leads")
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"inquiries", InquiryViewSet, basename="inquiries")

# Travel & Destination APIs
router.register(r"packages", TravelPackageViewSet, basename="packages")
router.register(r"destinations", DestinationViewSet, basename="destinations")

# Customer & Sales APIs
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"vouchers", VoucherViewSet, basename="vouchers")

# Resource APIs
router.register(r"resorts", ResortViewSet, basename="resorts")
router.register(r"meals", MealViewSet, basename="meals")
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"employees", EmployeeViewSet, basename="employees")

# Feedback API
router.register(r"feedback", FeedbackViewSet, basename="feedback")

urlpatterns = router.urls
