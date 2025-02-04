# Generated by Django 3.2.7 on 2021-10-01 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="competitions",
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
                ("title", models.CharField(max_length=150)),
                ("desc", models.TextField()),
                ("submissions", models.IntegerField()),
                ("lang", models.CharField(max_length=50)),
                ("date", models.DateField()),
            ],
        ),
    ]
