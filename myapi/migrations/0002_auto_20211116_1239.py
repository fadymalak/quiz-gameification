# Generated by Django 3.2.4 on 2021-11-16 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 23, 12, 39, 22, 275305)),
        ),
    ]
