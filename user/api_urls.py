from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    LoginAPIView,
    UserViewSet,
    CenterViewSet,
    CenterMinimalView,
    PlanViewSet,
    CustomerViewSet,
    SlotViewSet,
    SlotBookingViewSet,
    InvoiceViewSet,
    AdminDashboardView,
    BranchDashboardView,
    InvoiceExcelDownloadView,
    CustomerExcelDownloadView,
    AdminCustomerReportView,
    AdminSlotBookingReportView,
    BranchCustomerReportView,
    BranchSlotBookingReportView,
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
    path('centers/minimal/', CenterMinimalView.as_view(), name='center_minimal'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/branch/', BranchDashboardView.as_view(), name='branch_dashboard'),
    path('reports/admin/customers/', AdminCustomerReportView.as_view(), name='admin_customer_report'),
    path('reports/admin/slot-bookings/', AdminSlotBookingReportView.as_view(), name='admin_slot_booking_report'),
    path('reports/branch/customers/', BranchCustomerReportView.as_view(), name='branch_customer_report'),
    path('reports/branch/slot-bookings/', BranchSlotBookingReportView.as_view(), name='branch_slot_booking_report'),
    path('invoices/download/excel/', InvoiceExcelDownloadView.as_view(), name='invoice_excel_download'),
    path('invoices/<int:pk>/download/excel/', InvoiceExcelDownloadView.as_view(), name='invoice_excel_download_single'),
    path('customers/download/excel/', CustomerExcelDownloadView.as_view(), name='customer_excel_download'),
    path('customers/<int:pk>/download/excel/', CustomerExcelDownloadView.as_view(), name='customer_excel_download_single'),
    path('', include(router.urls)),
]