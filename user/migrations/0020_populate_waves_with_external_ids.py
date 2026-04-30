from django.db import migrations

def populate_waves(apps, schema_editor):
    Wave = apps.get_model('user', 'Wave')
    
    waves_data = [
        {'wave_name': 'Sexellence', 'external_id': 19},
        {'wave_name': 'Amrith', 'external_id': 18},
        {'wave_name': 'Zayana', 'external_id': 16},
        {'wave_name': 'Vikas', 'external_id': 15},
        {'wave_name': 'Aanandha', 'external_id': 21},
        {'wave_name': 'Relax', 'external_id': 23},
        {'wave_name': 'Samriddhi', 'external_id': 17},
        {'wave_name': 'Prabhav', 'external_id': 20},
    ]
    
    for wave_data in waves_data:
        Wave.objects.get_or_create(
            wave_name=wave_data['wave_name'],
            defaults={'external_id': wave_data['external_id']}
        )

def reverse_populate_waves(apps, schema_editor):
    Wave = apps.get_model('user', 'Wave')
    Wave.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_wave_external_id'),
    ]

    operations = [
        migrations.RunPython(populate_waves, reverse_populate_waves),
    ]
