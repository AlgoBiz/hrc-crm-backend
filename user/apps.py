from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from .models import User

        @receiver(post_save, sender=User)
        def set_superuser_role(sender, instance, **kwargs):
            if instance.is_superuser and instance.role != 'super_admin':
                User.objects.filter(pk=instance.pk).update(role='super_admin')
