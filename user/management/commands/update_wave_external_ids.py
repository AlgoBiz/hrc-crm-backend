from django.core.management.base import BaseCommand
from user.models import Wave

class Command(BaseCommand):
    help = 'Update Wave external IDs to match external API'

    def handle(self, *args, **options):
        wave_mapping = {
            'Sexellence': 19,
            'Amrith': 18,
            'Zayana': 16,
            'Vikas': 15,
            'Aanandha': 21,
            'Relax': 23,
            'Samriddhi': 17,
            'Prabhav': 20,
        }

        for wave_name, external_id in wave_mapping.items():
            try:
                wave = Wave.objects.get(wave_name=wave_name)
                wave.external_id = external_id
                wave.save()
                self.stdout.write(self.style.SUCCESS(f'Updated {wave_name} with external_id {external_id}'))
            except Wave.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Wave {wave_name} not found'))
