from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'user_panel'

urlpatterns = [
    path('', lambda request: redirect('user_panel:domestic', permanent=False)),
    path('international/', views.index, name='index'),
    path('domestic/', views.domestic, name='domestic'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('domestic/packages/', views.domestic_packages, name='domestic_packages'),
    path('international/packages/', views.international_packages, name='international_packages'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('hospitality/', views.hospitality, name='hospitality'),
  path('hospitality/<int:property_id>/', views.hospitality_detail, name='hospitality_detail'), 
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path('enquire-now/', views.enquire_now, name='enquire_now'),
    # user feedback form (simple page without sidebar)
    path('feedback-form/', views.feedback_form, name='feedback_form'),
    path('feedback_form/', views.feedback_form, name='feedback_form_alt'),  # support underscore variant
]