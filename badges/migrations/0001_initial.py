# Generated by Django 4.0.1 on 2022-01-23 21:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("image", models.ImageField(upload_to="upload/badges/")),
                ("points", models.IntegerField()),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="badges", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
