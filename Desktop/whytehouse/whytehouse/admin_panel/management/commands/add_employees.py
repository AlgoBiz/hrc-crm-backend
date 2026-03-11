from django.core.management.base import BaseCommand
from admin_panel.models import Employee
from datetime import date


class Command(BaseCommand):
    help = 'Add 5 sample employees to the database'

    def handle(self, *args, **kwargs):
        employees_data = [
            {
                'name': 'Rajesh Kumar',
                'role': 'Sales Manager',
                'email': 'rajesh.kumar@whytehouse.com',
                'phone': '9876543210',
                'department': 'Sales',
                'join_date': date(2024, 1, 15),
                'salary': 50000.00,
                'status': 'Active',
            },
            {
                'name': 'Priya Sharma',
                'role': 'Travel Consultant',
                'email': 'priya.sharma@whytehouse.com',
                'phone': '9876543211',
                'department': 'Operations',
                'join_date': date(2024, 3, 10),
                'salary': 35000.00,
                'status': 'Active',
            },
            {
                'name': 'Amit Patel',
                'role': 'Operations Manager',
                'email': 'amit.patel@whytehouse.com',
                'phone': '9876543212',
                'department': 'Operations',
                'join_date': date(2024, 2, 20),
                'salary': 45000.00,
                'status': 'Active',
            },
            {
                'name': 'Sneha Reddy',
                'role': 'Customer Support',
                'email': 'sneha.reddy@whytehouse.com',
                'phone': '9876543213',
                'department': 'Support',
                'join_date': date(2024, 5, 5),
                'salary': 30000.00,
                'status': 'Active',
            },
            {
                'name': 'Vikram Singh',
                'role': 'Marketing Executive',
                'email': 'vikram.singh@whytehouse.com',
                'phone': '9876543214',
                'department': 'Marketing',
                'join_date': date(2024, 4, 12),
                'salary': 32000.00,
                'status': 'Active',
            },
        ]

        created_count = 0
        for emp_data in employees_data:
            employee, created = Employee.objects.get_or_create(
                email=emp_data['email'],
                defaults=emp_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created employee: {employee.name} - {employee.role}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Employee already exists: {employee.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {created_count} new employee(s)!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total employees in database: {Employee.objects.count()}')
        )
