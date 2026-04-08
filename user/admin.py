from django.contrib import admin
from .models import Center, User, Customer, Plan, Invoice, Slot, SlotBooking


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('center_name', 'location', 'mobile', 'email', 'poc_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('center_name', 'location', 'mobile', 'email')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'center', 'is_active')
    list_filter = ('role', 'is_active', 'center')
    search_fields = ('username', 'email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'center', 'plan', 'wave', 'start_date', 'expiry_date', 'status')
    list_filter = ('status', 'center', 'city', 'state')
    search_fields = ('name', 'mobile', 'email')
    date_hierarchy = 'created_at'


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'duration_months', 'price', 'gst', 'status')
    list_filter = ('status',)
    search_fields = ('plan_name',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'customer', 'center', 'plan', 'amount', 'date', 'status', 'created_at')
    list_filter = ('status', 'center')
    search_fields = ('customer__name',)
    date_hierarchy = 'date'


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('center', 'start_time', 'end_time', 'booked_count', 'total_slot', 'status', 'is_enabled')
    list_filter = ('status', 'is_enabled', 'center')


@admin.register(SlotBooking)
class SlotBookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'slot', 'booking_date', 'status', 'created_at')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer__name',)
    date_hierarchy = 'booking_date'
