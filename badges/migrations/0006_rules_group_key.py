# Generated by Django 4.0.1 on 2022-04-04 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0005_remove_rules_variables_achievement_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='group_key',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]