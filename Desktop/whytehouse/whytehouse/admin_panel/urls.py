from . import views
from django.urls import path

app_name = 'admin_panel'

urlpatterns = [
    # Auth and main dashboard
    path('login/', views.login, name='login'), 
    path('forgot-password/', views.forgot_password, name='forgot_password'), 
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leads/', views.lead_management, name='leads'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/<int:lead_id>/', views.view_lead, name='view_lead'),
    path('leads/edit/<int:id>/', views.edit_lead, name='edit_lead'),
    path('leads/delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path("hospitality-management/", views.hospitality_management, name="admin_hospitality"),
    path("hospitality-management/add/", views.add_property, name="admin_add_property"),
    path("hospitality-management/<int:property_id>/", views.view_property, name="admin_view_property"),
    path("hospitality-management/edit/<int:property_id>/", views.edit_property, name="admin_edit_property"),
    path("hospitality-management/delete/<int:property_id>/", views.delete_property, name="admin_delete_property"),
    path("hospitality-management/toggle-status/<int:property_id>/", views.toggle_property_status, name="toggle_property_status"),
    path('travel-packages/', views.travel_packages, name='travel_packages'),
    path('travel-packages/add/', views.travel_package_add, name='travel_package_add'),
    path('travel-packages/<int:package_id>/', views.travel_package_view, name='travel_package_view'),
    path('travel-packages/edit/<int:package_id>/', views.travel_package_edit, name='travel_package_edit'),
    path('travel-packages/delete/<int:package_id>/', views.travel_package_delete, name='travel_package_delete'),
    path('travel-packages/toggle/<int:package_id>/', views.toggle_package_status, name='toggle_package_status'),
    # Destinations
    path('destinations/', views.destination_list, name='destinations'),
    path('destinations/add/', views.add_destination, name='add_destination'),
    path('destinations/<int:destination_id>/', views.view_destination, name='view_destination'),
    path('destinations/edit/<int:destination_id>/', views.edit_destination, name='edit_destination'),
    path('destinations/delete/<int:destination_id>/', views.delete_destination, name='delete_destination'),
    path('customer-inquiries/', views.customer_inquiries, name='customer_inquiries'),
    path('customer-inquiries/<int:inquiry_id>/', views.view_inquiry, name='view_inquiry'),
    path('customer-inquiries/<int:inquiry_id>/update-status/', views.update_inquiry_status, name='update_inquiry_status'),
]
#employee---------------
employee_patterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('<int:pk>/', views.view_employee, name='view_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
]

# SALES URL PATTERNS (to be included with 'sales' namespace in main urls.py)
sales_patterns = [
    #ACCOUNT URLS---------------------------------
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/<int:account_id>/', views.view_account, name='view_account'),
    path('accounts/<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('accounts/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    #CUSTOMER URLS---------------------------------
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:customer_id>/', views.view_customer, name='view_customer'),
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
    #RESORT URLS---------------------------------
    path('resorts/', views.resort_list, name='resort_list'),
    path('resorts/add/', views.add_resort, name='add_resort'),
    path('resorts/<int:resort_id>/', views.view_resort, name='view_resort'),
    path('resorts/<int:resort_id>/edit/', views.edit_resort, name='edit_resort'),
    path('resorts/<int:resort_id>/delete/', views.delete_resort, name='delete_resort'),
    #MEAL URLS---------------------------------
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/add/', views.add_meal, name='add_meal'),
    path('meals/<int:meal_id>/', views.view_meal, name='view_meal'),
    path('meals/<int:meal_id>/edit/', views.edit_meal, name='edit_meal'),
    path('meals/<int:meal_id>/delete/', views.delete_meal, name='delete_meal'),
    #VOUCHER URLS---------------------------------
    path('vouchers/', views.voucher_list, name='voucher_list'),
    path('vouchers/add/', views.add_voucher, name='add_voucher'),
    path('vouchers/<int:voucher_id>/', views.view_voucher, name='view_voucher'),
    path('vouchers/<int:voucher_id>/edit/', views.edit_voucher, name='edit_voucher'),
    path('vouchers/<int:voucher_id>/delete/', views.delete_voucher, name='delete_voucher'),
    #INVOICE URLS---------------------------------
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/add/', views.add_invoice, name='add_invoice'),
    path('invoices/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    path('invoices/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
    #REPORT URLS---------------------------------
    path('reports/invoice/', views.invoice_report, name='invoice_report'),
    path('reports/voucher/', views.voucher_report, name='voucher_report'),
    path('reports/leads/', views.leads_report, name='leads_report'),
    path('reports/profit/', views.profit_report, name='profit_report'),
    path('reports/customer/', views.customer_report, name='customer_report'),
]

# BLOG URL PATTERNS
blog_patterns = [
    path('blogs/', views.blog_list, name='blog_list'),  
    path('blogs/add/', views.add_blog, name='add_blog'),
    path('blogs/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('blogs/view/<slug:slug>/', views.view_blog, name='view_blog'),
    path('blogs/toggle-status/<int:blog_id>/', views.toggle_blog_status, name='toggle_blog_status'),
    path("blogs/category/add/", views.add_category, name="add_category"),
    path("blogs/category/delete/<int:category_id>/", views.delete_category, name="delete_category"),
]

# FEEDBACK URL PATTERNS
feedback_patterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('add/', views.add_feedback, name='add_feedback'),
    path('<int:feedback_id>/', views.view_feedback, name='view_feedback'),
    path('<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
    path('<int:feedback_id>/toggle-featured/', views.toggle_featured_feedback, name='toggle_featured_feedback'),
]
