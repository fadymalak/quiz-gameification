# Generated by Django 4.0.1 on 2022-03-28 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0019_remove_question_quiz_question_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gq",
            name="deleted",
            field=models.CharField(default="0", max_length=1),
        ),
        migrations.AlterField(
            model_name="mcq",
            name="deleted",
            field=models.CharField(default="0", max_length=1),
        ),
        migrations.AlterField(
            model_name="ynq",
            name="deleted",
            field=models.CharField(default="0", max_length=1),
        ),
    ]
