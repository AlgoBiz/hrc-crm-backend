from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        from user.models import User
        username = options.get('username')
        if not username:
            username = self.username_field.verbose_name
        try:
            user = User.objects.get(username=username)
            if user.role != 'super_admin':
                user.role = 'super_admin'
                user.save(update_fields=['role'])
                self.stdout.write(self.style.SUCCESS(f"Role set to 'super_admin' for user '{username}'"))
        except User.DoesNotExist:
            pass
