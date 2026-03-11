"""
URL configuration for whytehouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from admin_panel.urls import sales_patterns, employee_patterns, blog_patterns, feedback_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('user_panel.urls', 'user_panel'))),
    path('', include(('admin_panel.urls', 'admin_panel'))),
    
    # Sales URLs 
    path('sales/', include((sales_patterns, 'sales'))),
    # Employee URLs
    path('employee/', include((employee_patterns, 'employee'))),
    # Blog URLs (Admin)
    path('admin-blog/', include((blog_patterns, 'blog'))),
    # Feedback URLs (Admin)
    path('feedback/', include((feedback_patterns, 'feedback'))),

    #API URLS
    path("api/", include("admin_panel.api_urls")),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
   