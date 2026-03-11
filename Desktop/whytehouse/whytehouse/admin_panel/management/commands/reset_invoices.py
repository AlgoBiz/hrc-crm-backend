from django.core.management.base import BaseCommand
from admin_panel.models import Invoice, Customer, Resort, Account, Employee
from datetime import date, time, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Clear all invoices and add 10 sample invoices'

    def handle(self, *args, **kwargs):
        # Delete all existing invoices
        invoice_count = Invoice.objects.count()
        Invoice.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(f'🗑️  Deleted {invoice_count} existing invoice(s)')
        )

        # Check if we have required data
        customers = Customer.objects.all()
        resorts = Resort.objects.all()
        accounts = Account.objects.all()
        employees = Employee.objects.filter(status='Active')

        if not customers.exists():
            self.stdout.write(
                self.style.ERROR('❌ No customers found. Please add customers first.')
            )
            return

        if not resorts.exists():
            self.stdout.write(
                self.style.ERROR('❌ No resorts found. Please add resorts first.')
            )
            return

        if not accounts.exists():
            self.stdout.write(
                self.style.ERROR('❌ No accounts found. Please add accounts first.')
            )
            return

        if not employees.exists():
            self.stdout.write(
                self.style.ERROR('❌ No employees found. Please add employees first.')
            )
            return

        # Create 10 sample invoices
        today = date.today()
        
        invoices_data = []
        for i in range(1, 11):
            invoice_date = today - timedelta(days=(10 - i) * 3)  # Spread over last 30 days
            checkin_date = invoice_date + timedelta(days=5)
            checkout_date = checkin_date + timedelta(days=3)
            
            # Rotate through available data
            customer = customers[(i - 1) % customers.count()]
            resort = resorts[(i - 1) % resorts.count()]
            account = accounts[(i - 1) % accounts.count()]
            employee = employees[(i - 1) % employees.count()]
            
            # Calculate amounts
            nights = 3
            package_price = Decimal('15000.00') + (Decimal('1000.00') * i)
            tax = package_price * Decimal('0.12')  # 12% tax
            resort_price = Decimal('8000.00') + (Decimal('500.00') * i)
            total = package_price + tax
            received = total * Decimal('0.6')  # 60% paid
            pending = total - received
            profit = package_price - resort_price
            
            invoices_data.append({
                'customer': customer,
                'invoice_no': f'INV-2026-{str(i).zfill(3)}',
                'invoice_date': invoice_date,
                'sales_person': employee,
                'resort': resort,
                'checkin_date': checkin_date,
                'checkout_date': checkout_date,
                'checkin_time': time(14, 0),  # 2:00 PM
                'checkout_time': time(11, 0),  # 11:00 AM
                'adults': 2,
                'children': 1 if i % 2 == 0 else 0,
                'pax_total': 3 if i % 2 == 0 else 2,
                'pax_notes': f'Family booking - Invoice {i}',
                'nights': nights,
                'room_type': 'Deluxe' if i % 2 == 0 else 'Standard',
                'rooms': 1,
                'meals_plan': 'Full Board' if i % 3 == 0 else 'Half Board',
                'bank_account': account,
                'package_price': package_price,
                'tax': tax,
                'resort_price': resort_price,
                'total': total,
                'received': received,
                'pending': pending,
                'profit': profit,
                'notes': f'Sample invoice {i} - Generated for testing',
            })

        # Create invoices
        created_count = 0
        for inv_data in invoices_data:
            try:
                invoice = Invoice.objects.create(**inv_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created invoice: {invoice.invoice_no} - '
                        f'{invoice.customer.display_name} - '
                        f'₹{invoice.total}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating invoice: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {created_count} invoice(s)!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total invoices in database: {Invoice.objects.count()}')
        )
        
        # Show summary
        total_amount = sum(inv['total'] for inv in invoices_data)
        total_received = sum(inv['received'] for inv in invoices_data)
        total_pending = sum(inv['pending'] for inv in invoices_data)
        
        self.stdout.write('\n📈 Financial Summary:')
        self.stdout.write(f'   Total Amount: ₹{total_amount:,.2f}')
        self.stdout.write(f'   Received: ₹{total_received:,.2f}')
        self.stdout.write(f'   Pending: ₹{total_pending:,.2f}')
