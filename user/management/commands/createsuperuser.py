from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        from user.models import User
        # After superuser creation, find the latest superuser and set role
        try:
            user = User.objects.filter(is_superuser=True).latest('date_joined')
            if user.role != 'super_admin':
                user.role = 'super_admin'
                user.save(update_fields=['role'])
                self.stdout.write(self.style.SUCCESS(f"Role set to 'super_admin' for user '{user.username}'"))
        except User.DoesNotExist:
            pass
