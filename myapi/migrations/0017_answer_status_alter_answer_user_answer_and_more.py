# Generated by Django 4.0.1 on 2022-03-21 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0016_question_point_alter_question_content_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='status',
            field=models.TextField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], default='COMPLETED'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user_answer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='ynq',
            name='correct_answer',
            field=models.CharField(choices=[('T', 'True'), ('F', 'False')], max_length=1),
        ),
    ]
