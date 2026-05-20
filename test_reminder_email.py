"""
Test script to check email sending for plan expiry reminders
Run with: python manage.py shell < test_reminder_email.py
"""

from datetime import date, timedelta
from user.models import Customer
from user.utils import send_plan_expiry_reminder

print("\n" + "="*60)
print("TESTING PLAN EXPIRY REMINDER EMAIL SYSTEM")
print("="*60 + "\n")

# Check for customers with upcoming expiry dates
today = date.today()
reminder_days = [30, 15, 2]

print(f"Today's date: {today}\n")

for days in reminder_days:
    target_date = today + timedelta(days=days)
    customers = Customer.objects.filter(
        expiry_date=target_date,
        plan__isnull=False
    ).select_related('plan')
    
    count = customers.count()
    print(f"📅 Customers expiring in {days} days ({target_date}): {count}")
    
    if count > 0:
        for customer in customers:
            print(f"   - {customer.name} ({customer.email}) - Plan: {customer.plan.name}")

print("\n" + "-"*60)
print("SENDING TEST EMAIL")
print("-"*60 + "\n")

# Try to send a test email to the first customer found
test_customer = None
test_days = None

for days in reminder_days:
    target_date = today + timedelta(days=days)
    customers = Customer.objects.filter(
        expiry_date=target_date,
        plan__isnull=False,
        email__isnull=False
    ).select_related('plan').first()
    
    if customers:
        test_customer = customers
        test_days = days
        break

if test_customer:
    print(f"Sending test email to: {test_customer.name} ({test_customer.email})")
    print(f"Days until expiry: {test_days}")
    print(f"Plan: {test_customer.plan.name}")
    print(f"Expiry date: {test_customer.expiry_date}\n")
    
    success = send_plan_expiry_reminder(test_customer, test_days)
    
    if success:
        print("✅ Email sent successfully!")
        print("\nCheck:")
        print(f"1. Email inbox: {test_customer.email}")
        print("2. Celery worker logs for any errors")
        print("3. Django logs for email backend messages")
    else:
        print("❌ Email sending failed!")
        print("Check your email configuration in .env file")
else:
    print("⚠️  No customers found with expiry dates in 30, 15, or 2 days")
    print("\nTo test the email system:")
    print("1. Create a test customer with an expiry date 30 days from today")
    print("2. Or manually call send_plan_expiry_reminder() with a customer object")
    print("\nExample:")
    print(">>> from user.models import Customer")
    print(">>> from user.utils import send_plan_expiry_reminder")
    print(">>> customer = Customer.objects.filter(email__isnull=False).first()")
    print(">>> send_plan_expiry_reminder(customer, 30)")

print("\n" + "="*60 + "\n")
