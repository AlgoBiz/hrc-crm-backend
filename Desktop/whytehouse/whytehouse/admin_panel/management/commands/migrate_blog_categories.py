from django.core.management.base import BaseCommand
from admin_panel.models import BlogCategory

class Command(BaseCommand):
    help = 'Create default blog categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Destinations', 'order': 1},
            {'name': 'Travel Tips', 'order': 2},
            {'name': 'Food & Culture', 'order': 3},
            {'name': 'Packages & Deals', 'order': 4},
            {'name': 'Honeymoon', 'order': 5},
            {'name': 'Family Travel', 'order': 6},
            {'name': 'Adventure', 'order': 7},
            {'name': 'Travel Stories', 'order': 8},
            {'name': 'Other', 'order': 9},
        ]
        
        for cat_data in categories:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'order': cat_data['order'], 'is_active': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  Category already exists: {category.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ All categories created!'))
