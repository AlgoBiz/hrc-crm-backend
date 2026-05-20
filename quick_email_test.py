"""
Quick email test - Run in Django shell
Copy and paste these commands one by one
"""

# Step 1: Import required modules
from user.models import Customer
from user.utils import send_plan_expiry_reminder

# Step 2: List all customers with email
print("\n📋 Customers with email addresses:")
customers = Customer.objects.filter(email__isnull=False).exclude(email='')
for i, c in enumerate(customers[:20], 1):
    plan_name = c.plan.name if c.plan else "No Plan"
    print(f"{i}. {c.name} - {c.email} - {plan_name}")

# Step 3: Pick a customer (change the number below)
# Example: customer = Customer.objects.get(email="test@example.com")
customer = customers.first()  # Gets the first customer

if customer:
    print(f"\n✅ Selected: {customer.name} ({customer.email})")
    
    # Step 4: Send test email
    print("\n📧 Sending test reminder email...")
    result = send_plan_expiry_reminder(customer, 30)
    
    if result:
        print(f"✅ SUCCESS! Email sent to {customer.email}")
        print("Check the inbox (and spam folder)")
    else:
        print("❌ FAILED! Check email configuration")
else:
    print("❌ No customers found")
