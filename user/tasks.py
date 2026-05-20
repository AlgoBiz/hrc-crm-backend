from celery import shared_task
from datetime import date, timedelta
from .models import Customer
from .utils import send_plan_expiry_reminder


@shared_task
def send_expiry_reminders():
    """Send plan expiry reminder emails at 30, 15, and 2 days before expiry"""
    
    today = date.today()
    
    # Days to check: 30, 15, 2
    reminder_days = [30, 15, 2]
    
    total_sent = 0
    
    for days in reminder_days:
        target_date = today + timedelta(days=days)
        
        # Find customers whose plan expires on target date
        customers = Customer.objects.filter(
            expiry_date=target_date,
            plan__isnull=False
        ).select_related('plan')
        
        for customer in customers:
            if customer.email:
                success = send_plan_expiry_reminder(customer, days)
                if success:
                    total_sent += 1
                    print(f'Sent {days}-day reminder to {customer.name} ({customer.email})')
    
    print(f'Successfully sent {total_sent} reminder emails')
    return f'Sent {total_sent} emails'
