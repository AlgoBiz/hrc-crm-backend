from django.urls import path

from .api_views import (
    customer_list_create,
    customer_detail,
    LoginAPIView,
    plan_list_create,
    plan_detail,
    CenterListCreateAPIView,
    CenterDetailAPIView,
    SlotListCreateAPIView,
    SlotDetailAPIView,
    SlotBookingListCreateAPIView,
    SlotBookingDetailAPIView,
    invoice_list_create,
    invoice_detail,
)

urlpatterns = [
    path('customers/', customer_list_create),
    path('customers/<int:pk>/', customer_detail),
    path("login/", LoginAPIView.as_view(), name="login"),

    path('plans/', plan_list_create),
    path('plans/<int:pk>/', plan_detail),

    path("centers/", CenterListCreateAPIView.as_view(), name="center_list_create"),
    path("centers/<int:pk>/", CenterDetailAPIView.as_view(), name="center_detail"),

    path("slots/", SlotListCreateAPIView.as_view(), name="slots"),
    path("slots/<int:pk>/", SlotDetailAPIView.as_view(), name="slot_detail"),

    path("slot-bookings/", SlotBookingListCreateAPIView.as_view(), name="slot_bookings"),
    path("slot-bookings/<int:pk>/", SlotBookingDetailAPIView.as_view(), name="slot_booking_detail"),

    path('invoices/', invoice_list_create),
    path('invoices/<int:pk>/', invoice_detail),
]
    



