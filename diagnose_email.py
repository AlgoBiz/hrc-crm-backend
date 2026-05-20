"""
Email Diagnostic Script - Find out why emails aren't being sent
Run with: python manage.py shell < diagnose_email.py
"""

import os
from django.conf import settings
from django.core.mail import send_mail
from user.models import Customer

print("\n" + "="*70)
print("EMAIL CONFIGURATION DIAGNOSTIC")
print("="*70 + "\n")

# 1. Check Email Settings
print("📧 EMAIL CONFIGURATION:")
print(f"   Backend: {settings.EMAIL_BACKEND}")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   Port: {settings.EMAIL_PORT}")
print(f"   Use TLS: {settings.EMAIL_USE_TLS}")
print(f"   Host User: {settings.EMAIL_HOST_USER}")
print(f"   Host Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"   From Email: {settings.DEFAULT_FROM_EMAIL}")

# 2. Check if credentials are set
print("\n" + "-"*70)
print("🔑 CREDENTIAL CHECK:")
if not settings.EMAIL_HOST_USER:
    print("   ❌ EMAIL_HOST_USER is not set in .env file")
else:
    print(f"   ✅ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

if not settings.EMAIL_HOST_PASSWORD:
    print("   ❌ EMAIL_HOST_PASSWORD is not set in .env file")
else:
    print(f"   ✅ EMAIL_HOST_PASSWORD: Set (hidden)")

# 3. Test basic email sending
print("\n" + "-"*70)
print("📨 TESTING BASIC EMAIL SENDING:")

test_email = settings.EMAIL_HOST_USER  # Send to yourself for testing

if test_email:
    print(f"   Sending test email to: {test_email}")
    
    try:
        result = send_mail(
            subject='Test Email from HRC CRM',
            message='This is a test email. If you receive this, email configuration is working!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        if result == 1:
            print(f"   ✅ TEST EMAIL SENT SUCCESSFULLY!")
            print(f"   Check inbox: {test_email}")
            print(f"   Also check spam/junk folder")
        else:
            print(f"   ⚠️  Email function returned: {result}")
            
    except Exception as e:
        print(f"   ❌ ERROR SENDING EMAIL:")
        print(f"   {type(e).__name__}: {str(e)}")
        print("\n   Common issues:")
        print("   1. Gmail: Need to use App Password (not regular password)")
        print("   2. Gmail: Enable 2-Step Verification first")
        print("   3. SMTP blocked by firewall/antivirus")
        print("   4. Wrong credentials in .env file")
else:
    print("   ❌ Cannot test - EMAIL_HOST_USER not set")

# 4. Check customers
print("\n" + "-"*70)
print("👥 CUSTOMER CHECK:")
customers_with_email = Customer.objects.filter(email__isnull=False).exclude(email='')
print(f"   Total customers with email: {customers_with_email.count()}")

if customers_with_email.exists():
    print("\n   Sample customers:")
    for c in customers_with_email[:5]:
        plan_name = c.plan.plan_name if c.plan else "No Plan"
        print(f"   - {c.name} ({c.email}) - {plan_name}")

# 5. Gmail App Password Instructions
print("\n" + "="*70)
print("🔧 TROUBLESHOOTING GUIDE:")
print("="*70)

if 'gmail' in settings.EMAIL_HOST.lower():
    print("\n📌 FOR GMAIL USERS:")
    print("   Gmail requires an 'App Password' (not your regular password)")
    print("\n   Steps to create App Password:")
    print("   1. Go to: https://myaccount.google.com/security")
    print("   2. Enable '2-Step Verification' (if not already enabled)")
    print("   3. Go to: https://myaccount.google.com/apppasswords")
    print("   4. Select 'Mail' and 'Windows Computer'")
    print("   5. Click 'Generate'")
    print("   6. Copy the 16-character password")
    print("   7. Update .env file:")
    print("      EMAIL_HOST_PASSWORD=your-16-char-app-password")
    print("   8. Restart Django and Celery")

print("\n📌 COMMON ISSUES:")
print("   1. Wrong email/password in .env")
print("   2. Gmail: Using regular password instead of App Password")
print("   3. Firewall/antivirus blocking SMTP port 587")
print("   4. Email provider requires 'Less secure app access'")
print("   5. Customer email address is invalid")

print("\n📌 QUICK FIX:")
print("   For testing, use console backend (emails print to console):")
print("   Add to .env: EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend")

print("\n" + "="*70 + "\n")
