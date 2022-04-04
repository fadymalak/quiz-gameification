# Generated by Django 4.0.1 on 2022-03-31 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0003_achievement_achievementlevel_rules_userachievement_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariableUserDetials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveBigIntegerField()),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('variable_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detials', to='badges.variableuser')),
            ],
        ),
    ]