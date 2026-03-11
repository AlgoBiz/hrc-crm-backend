from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from admin_panel.models import Account, Customer, Resort, Meal, Voucher, Invoice, Employee, Lead
from user_panel.models import Blog


class Command(BaseCommand):
    help = 'Add 5 sample records for each model'

    def handle(self, *args, **kwargs):
        # Accounts
        accounts = []
        for i in range(1, 6):
            acc, _ = Account.objects.get_or_create(
                account_number=f'ACC{i:012d}',
                defaults={
                    'account_name': f'Account {i}',
                    'bank_name': ['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB'][i-1],
                    'ifsc_code': f'BANK000{i}234',
                    'account_type': 'current' if i % 2 else 'savings'
                }
            )
            accounts.append(acc)
        self.stdout.write('✓ 5 Accounts')

        # Resorts
        resorts = []
        locations = ['Goa', 'Jaipur', 'Munnar', 'Manali', 'Udaipur']
        for i in range(1, 6):
            resort, _ = Resort.objects.get_or_create(
                resort_name=f'Resort {i}',
                defaults={
                    'location': locations[i-1],
                    'contact_person': f'Manager {i}',
                    'contact_number': f'98765432{i:02d}',
                    'email': f'resort{i}@example.com',
                    'address': f'Address {i}, {locations[i-1]}',
                    'status': 'Active'
                }
            )
            resorts.append(resort)
        self.stdout.write('✓ 5 Resorts')

        # Meals
        meals = []
        meal_types = [
            ('EP', 'European Plan', 'None'),
            ('CP', 'Continental Plan', 'Breakfast'),
            ('MAP', 'Modified American Plan', 'Breakfast, Dinner'),
            ('AP', 'American Plan', 'All Meals'),
            ('AI', 'All Inclusive', 'All Meals + Drinks')
        ]
        for i, (name, desc, included) in enumerate(meal_types, 1):
            meal, _ = Meal.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'included_meals': included,
                    'status': 'Available'
                }
            )
            meals.append(meal)
        self.stdout.write('✓ 5 Meals')

        # Employees
        employees = []
        for i in range(1, 6):
            emp, _ = Employee.objects.get_or_create(
                email=f'emp{i}@whytehouse.com',
                defaults={
                    'name': f'Employee {i}',
                    'role': ['Manager', 'Sales', 'Support', 'Admin', 'Agent'][i-1],
                    'phone': f'91234567{i:02d}',
                    'status': 'Active'
                }
            )
            employees.append(emp)
        self.stdout.write('✓ 5 Employees')

        # Customers
        customers = []
        for i in range(1, 6):
            cust, _ = Customer.objects.get_or_create(
                email=f'customer{i}@example.com',
                defaults={
                    'display_name': f'Customer {i}',
                    'phone': f'98000000{i:02d}',
                    'address': f'Address {i}',
                    'city': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'][i-1],
                    'state': ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal'][i-1],
                    'pincode': f'40000{i}',
                    'status': 'Active'
                }
            )
            customers.append(cust)
        self.stdout.write('✓ 5 Customers')

        # Leads
        for i in range(1, 6):
            Lead.objects.get_or_create(
                email=f'lead{i}@example.com',
                defaults={
                    'name': f'Lead {i}',
                    'phone': f'97000000{i:02d}',
                    'message': f'Interested in package {i}',
                    'status': ['New', 'Contacted', 'Qualified', 'Converted', 'Lost'][i-1]
                }
            )
        self.stdout.write('✓ 5 Leads')

        # Blogs
        for i in range(1, 6):
            Blog.objects.get_or_create(
                title=f'Blog Post {i}',
                defaults={
                    'content': f'This is sample blog content for post {i}. ' * 10,
                    'author': f'Author {i}',
                    'published_date': timezone.now().date() - timedelta(days=i*10),
                    'status': 'Published'
                }
            )
        self.stdout.write('✓ 5 Blogs')

        # Invoices
        for i in range(1, 6):
            date = timezone.now().date() - timedelta(days=i*5)
            Invoice.objects.get_or_create(
                invoice_no=f'INV-{date.strftime("%Y%m")}-{i:04d}',
                defaults={
                    'customer': customers[i-1],
                    'invoice_date': date,
                    'sales_person': employees[i-1],
                    'resort': resorts[i-1],
                    'checkin_date': date + timedelta(days=7),
                    'checkout_date': date + timedelta(days=10),
                    'checkin_time': '14:00',
                    'checkout_time': '11:00',
                    'adults': 2,
                    'children': 1,
                    'pax_total': 3,
                    'nights': 3,
                    'room_type': 'Deluxe',
                    'rooms': 1,
                    'meals_plan': 'CP',
                    'bank_account': accounts[i-1],
                    'package_price': Decimal('10000'),
                    'tax': Decimal('1800'),
                    'resort_price': Decimal('7000'),
                    'total': Decimal('11800'),
                    'received': Decimal('11800'),
                    'pending': Decimal('0'),
                    'profit': Decimal('3000')
                }
            )
        self.stdout.write('✓ 5 Invoices')

        # Vouchers
        for i in range(1, 6):
            date = timezone.now().date() - timedelta(days=i*3)
            Voucher.objects.get_or_create(
                voucher_no=f'VCH-{date.strftime("%Y%m")}-{i:04d}',
                defaults={
                    'customer': customers[i-1],
                    'voucher_date': date,
                    'sales_person': employees[i-1],
                    'resort': resorts[i-1],
                    'checkin_date': date + timedelta(days=5),
                    'checkout_date': date + timedelta(days=8),
                    'checkin_time': '14:00',
                    'checkout_time': '11:00',
                    'adults': 2,
                    'children': 0,
                    'nights': 3,
                    'room_type': 'Suite',
                    'no_of_rooms': 1,
                    'meals_plan': meals[i-1],
                    'bank_account': accounts[i-1],
                    'package_price': Decimal('15000'),
                    'resort_price': Decimal('10000'),
                    'total_amount': Decimal('15000'),
                    'received': Decimal('15000'),
                    'pending': Decimal('0'),
                    'from_whytehouse': Decimal('2000'),
                    'profit': Decimal('3000')
                }
            )
        self.stdout.write('✓ 5 Vouchers')

        self.stdout.write(self.style.SUCCESS('\nSample data added successfully!'))
