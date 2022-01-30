# Generated by Django 4.0.1 on 2022-01-17 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0006_alter_quiz_end_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 24, 9, 3, 0, 816474)),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False),
        ),
    ]
