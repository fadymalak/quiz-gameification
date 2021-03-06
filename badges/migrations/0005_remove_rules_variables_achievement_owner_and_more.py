# Generated by Django 4.0.1 on 2022-04-02 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('badges', '0004_variableuserdetials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rules',
            name='variables',
        ),
        migrations.AddField(
            model_name='achievement',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievementlevel',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rules',
            name='variable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rule', to='badges.variable'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userachievement',
            name='achievement_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='badges.achievementlevel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='achievementlevel',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='badges.achievementlevel'),
        ),
        migrations.AlterField(
            model_name='rules',
            name='achievement_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='badges.achievementlevel'),
        ),
    ]
