"""
Send a test reminder email to a specific customer
Usage: python manage.py shell < send_test_reminder.py
"""

from user.models import Customer
from user.utils import send_plan_expiry_reminder

print("\n" + "="*60)
print("SEND TEST REMINDER EMAIL TO CUSTOMER")
print("="*60 + "\n")

# Change this to the customer email you want to test
TEST_EMAIL = "customer@example.com"  # ← CHANGE THIS TO YOUR TEST EMAIL

print(f"Looking for customer with email: {TEST_EMAIL}\n")

try:
    customer = Customer.objects.get(email=TEST_EMAIL)
    
    print(f"✅ Customer found!")
    print(f"   Name: {customer.name}")
    print(f"   Email: {customer.email}")
    print(f"   Phone: {customer.phone}")
    
    if customer.plan:
        print(f"   Plan: {customer.plan.name}")
        print(f"   Expiry Date: {customer.expiry_date}")
    else:
        print(f"   ⚠️  No plan assigned")
    
    print(f"\n📧 Sending test reminder email (30-day reminder)...\n")
    
    # Send test email with 30 days reminder
    success = send_plan_expiry_reminder(customer, 30)
    
    if success:
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print(f"\nCheck the inbox: {customer.email}")
        print("Also check spam/junk folder if not in inbox")
    else:
        print("❌ EMAIL SENDING FAILED!")
        print("\nPossible reasons:")
        print("1. Email configuration issue in .env file")
        print("2. SMTP credentials incorrect")
        print("3. Network/firewall blocking SMTP")
        print("4. Customer has no plan assigned")
        
except Customer.DoesNotExist:
    print(f"❌ No customer found with email: {TEST_EMAIL}")
    print("\nAvailable customers with email:")
    
    customers = Customer.objects.filter(email__isnull=False).exclude(email='')[:10]
    
    if customers.exists():
        for c in customers:
            plan_name = c.plan.name if c.plan else "No Plan"
            print(f"   - {c.name} ({c.email}) - {plan_name}")
    else:
        print("   No customers with email addresses found")
    
    print("\n💡 Update TEST_EMAIL in this script and run again")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60 + "\n")
