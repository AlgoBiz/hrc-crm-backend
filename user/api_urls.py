from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    LoginAPIView,
    UserViewSet,
    CenterViewSet,
    PlanViewSet,
    CustomerViewSet,
    SlotViewSet,
    SlotBookingViewSet,
    InvoiceViewSet,
    AdminDashboardView,
    BranchDashboardView,
    CustomerReportView,
    SlotBookingReportView,
    InvoiceExcelDownloadView,
    CustomerExcelDownloadView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'centers', CenterViewSet, basename='center')
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'slots', SlotViewSet, basename='slot')
router.register(r'slot-bookings', SlotBookingViewSet, basename='slot-booking')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/branch/', BranchDashboardView.as_view(), name='branch_dashboard'),
    path('reports/customers/', CustomerReportView.as_view(), name='customer_report'),
    path('reports/slot-bookings/', SlotBookingReportView.as_view(), name='slot_booking_report'),
    path('invoices/download/excel/', InvoiceExcelDownloadView.as_view(), name='invoice_excel_download'),
    path('invoices/<int:pk>/download/excel/', InvoiceExcelDownloadView.as_view(), name='invoice_excel_download_single'),
    path('customers/download/excel/', CustomerExcelDownloadView.as_view(), name='customer_excel_download'),
    path('customers/<int:pk>/download/excel/', CustomerExcelDownloadView.as_view(), name='customer_excel_download_single'),
    path('', include(router.urls)),
]