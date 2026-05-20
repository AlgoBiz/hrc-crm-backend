from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from user.models import Customer
from user.utils import send_plan_expiry_reminder


class Command(BaseCommand):
    help = 'Send plan expiry reminder emails'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Days to check: 30, 7, 2
        reminder_days = [30, 7, 2]
        
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
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Sent {days}-day reminder to {customer.name} ({customer.email})'
                            )
                        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent {total_sent} reminder emails'
            )
        )
