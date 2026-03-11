from django.shortcuts import redirect
from django.urls import reverse

class AdminOTPVerificationMiddleware:
    """
    Middleware to ensure admin users have completed OTP verification
    before accessing any admin panel views except login, verify-otp, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require OTP verification
        self.auth_urls = [
            '/login/',
            '/verify-otp/',
            '/resend-otp/',
            '/forgot-password/',
        ]
    
    def __call__(self, request):
        # Only apply to admin_panel URLs
        if request.path.startswith('/dashboard/') or \
           request.path.startswith('/leads/') or \
           request.path.startswith('/hospitality-management/') or \
           request.path.startswith('/travel-packages/') or \
           request.path.startswith('/destinations/') or \
           request.path.startswith('/customer-inquiries/') or \
           request.path.startswith('/employee/') or \
           request.path.startswith('/sales/') or \
           request.path.startswith('/admin-blog/') or \
           request.path.startswith('/feedback/'):
            
            # Check if user has completed OTP verification
            otp_verified = request.session.get('admin_otp_verified', False)
            
            if not otp_verified:
                # Redirect to login if not verified
                return redirect('admin_panel:login')
        
        response = self.get_response(request)
        return response
