# Generated by Django 3.2.7 on 2021-10-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_submissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="submissions",
            name="pgid",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
