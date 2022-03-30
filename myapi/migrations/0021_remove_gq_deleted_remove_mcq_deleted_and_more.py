# Generated by Django 4.0.1 on 2022-03-29 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0020_alter_gq_deleted_alter_mcq_deleted_alter_ynq_deleted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gq",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="mcq",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="ynq",
            name="deleted",
        ),
        migrations.AddField(
            model_name="question",
            name="deleted",
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name="question",
            name="quiz",
        ),
        migrations.AddField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="myapi.quiz",
            ),
            preserve_default=False,
        ),
    ]
