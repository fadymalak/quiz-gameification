# Generated by Django 4.0.1 on 2022-03-07 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("myapi", "0012_alter_quiz_end_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="correct_answer",
        ),
        migrations.RemoveField(
            model_name="question",
            name="option1",
        ),
        migrations.RemoveField(
            model_name="question",
            name="option2",
        ),
        migrations.RemoveField(
            model_name="question",
            name="option3",
        ),
        migrations.RemoveField(
            model_name="question",
            name="option4",
        ),
        migrations.AddField(
            model_name="gq",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to={"model__in": ("mcq", "gq", "ynq")},
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="qid",
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AddField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="myapi.quiz",
            ),
        ),
        migrations.AddField(
            model_name="ynq",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="MCQ",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.IntegerField(default=0)),
                ("title", models.TextField()),
                ("image", models.ImageField(default="", upload_to="")),
                ("option1", models.CharField(max_length=150)),
                ("option2", models.CharField(max_length=150)),
                ("option3", models.CharField(max_length=150)),
                ("option4", models.CharField(max_length=150)),
                ("correct_answer", models.TextField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
