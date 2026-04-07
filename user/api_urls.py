from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .api_views import (
    wave_choices,
    customer_list, customer_create, customer_detail, customer_update, customer_delete,
    LoginAPIView,
    plan_list, plan_create, plan_detail, plan_update, plan_delete,
    CenterListCreateAPIView, CenterDetailAPIView,
    SlotListCreateAPIView, SlotDetailAPIView,
    SlotBookingListCreateAPIView, SlotBookingDetailAPIView,
    invoice_list, invoice_create, invoice_detail, invoice_update, invoice_delete,
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
    path('customers/<int:pk>/delete/', customer_delete),

    # Plans
    path('plans/', plan_list),
    path('plans/create/', plan_create),
    path('plans/<int:pk>/', plan_detail),
    path('plans/<int:pk>/update/', plan_update),
    path('plans/<int:pk>/delete/', plan_delete),

    # Centers
    path('centers/', CenterListCreateAPIView.as_view(), name='center_list'),
    path('centers/create/', CenterListCreateAPIView.as_view(), name='center_create'),
    path('centers/<int:pk>/', CenterDetailAPIView.as_view(), name='center_detail'),

    # Slots
    path('slots/', SlotListCreateAPIView.as_view(), name='slot_list'),
    path('slots/create/', SlotListCreateAPIView.as_view(), name='slot_create'),
    path('slots/<int:pk>/', SlotDetailAPIView.as_view(), name='slot_detail'),

    # Slot Bookings
    path('slot-bookings/', SlotBookingListCreateAPIView.as_view(), name='slot_booking_list'),
    path('slot-bookings/create/', SlotBookingListCreateAPIView.as_view(), name='slot_booking_create'),
    path('slot-bookings/<int:pk>/', SlotBookingDetailAPIView.as_view(), name='slot_booking_detail'),

    # Invoices
    path('invoices/', invoice_list),
    path('invoices/create/', invoice_create),
    path('invoices/<int:pk>/', invoice_detail),
    path('invoices/<int:pk>/update/', invoice_update),
    path('invoices/<int:pk>/delete/', invoice_delete),
]
    



