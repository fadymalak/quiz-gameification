# Generated by Django 4.0.4 on 2022-05-25 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0022_alter_courses_id_alter_quiz_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gq',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='mcq',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ynq',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
