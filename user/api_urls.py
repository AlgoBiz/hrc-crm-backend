from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .api_views import (
    wave_choices,
    customer_list, customer_create, customer_detail, customer_update, customer_partial_update, customer_delete,
    LoginAPIView,
    plan_list, plan_create, plan_detail, plan_update, plan_partial_update, plan_delete,
    center_list, center_create, center_detail, center_update, center_partial_update, center_delete,
    slot_list, slot_create, slot_detail, slot_update, slot_partial_update, slot_delete,
    slot_booking_list, slot_booking_create, slot_booking_detail, slot_booking_update, slot_booking_partial_update, slot_booking_delete,
    invoice_list, invoice_create, invoice_detail, invoice_update, invoice_partial_update, invoice_delete,
    dashboard_summary, dashboard_centerwise_performance, dashboard_revenue_overview, dashboard_membership_status,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Customers
    path('customers/wave-choices/', wave_choices),
    path('customers/', customer_list),
    path('customers/create/', customer_create),
    path('customers/<int:pk>/', customer_detail),
    path('customers/<int:pk>/update/', customer_update),
    path('customers/<int:pk>/patch/', customer_partial_update),
    path('customers/<int:pk>/delete/', customer_delete),

    # Plans
    path('plans/', plan_list),
    path('plans/create/', plan_create),
    path('plans/<int:pk>/', plan_detail),
    path('plans/<int:pk>/update/', plan_update),
    path('plans/<int:pk>/patch/', plan_partial_update),
    path('plans/<int:pk>/delete/', plan_delete),

    # Centers
    path('centers/', center_list),
    path('centers/create/', center_create),
    path('centers/<int:pk>/', center_detail),
    path('centers/<int:pk>/update/', center_update),
    path('centers/<int:pk>/patch/', center_partial_update),
    path('centers/<int:pk>/delete/', center_delete),

    # Slots
    path('slots/', slot_list),
    path('slots/create/', slot_create),
    path('slots/<int:pk>/', slot_detail),
    path('slots/<int:pk>/update/', slot_update),
    path('slots/<int:pk>/patch/', slot_partial_update),
    path('slots/<int:pk>/delete/', slot_delete),

    # Slot Bookings
    path('slot-bookings/', slot_booking_list),
    path('slot-bookings/create/', slot_booking_create),
    path('slot-bookings/<int:pk>/', slot_booking_detail),
    path('slot-bookings/<int:pk>/update/', slot_booking_update),
    path('slot-bookings/<int:pk>/patch/', slot_booking_partial_update),
    path('slot-bookings/<int:pk>/delete/', slot_booking_delete),

    # Invoices
    path('invoices/', invoice_list),
    path('invoices/create/', invoice_create),
    path('invoices/<int:pk>/', invoice_detail),
    path('invoices/<int:pk>/update/', invoice_update),
    path('invoices/<int:pk>/patch/', invoice_partial_update),
    path('invoices/<int:pk>/delete/', invoice_delete),

    # Dashboard
    path('dashboard/summary/', dashboard_summary),
    path('dashboard/centerwise-performance/', dashboard_centerwise_performance),
    path('dashboard/revenue-overview/', dashboard_revenue_overview),
    path('dashboard/membership-status/', dashboard_membership_status),
]
    



