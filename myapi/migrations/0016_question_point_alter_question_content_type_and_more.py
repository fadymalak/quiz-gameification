# Generated by Django 4.0.1 on 2022-03-19 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("myapi", "0015_remove_question_created_at_remove_question_deleted_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="point",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="question",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to={"model__in": ("mcq", "gq", "ynq")},
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="qid",
            field=models.PositiveBigIntegerField(auto_created=True),
        ),
    ]
