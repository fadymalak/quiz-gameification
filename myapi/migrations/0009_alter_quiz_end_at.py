# Generated by Django 4.0.1 on 2022-01-23 21:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0008_alter_user_managers_alter_answer_id_alter_courses_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="end_at",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 1, 30, 23, 31, 22, 270172)
            ),
        ),
    ]
