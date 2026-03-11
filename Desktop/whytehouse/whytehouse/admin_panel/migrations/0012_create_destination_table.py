from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0011_auto_20260228_1023"),
    ]

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("country", models.CharField(max_length=100)),
                ("category", models.CharField(choices=[("Domestic", "Domestic"), ("International", "International")], default="Domestic", max_length=20)),
                ("description", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="destinations/")),
                ("is_popular", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]