# Generated by Django 4.0.1 on 2022-03-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0011_gq_ynq_remove_question_point_remove_question_quiz_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="end_at",
            field=models.DateTimeField(),
        ),
    ]
