# Generated by Django 3.2.7 on 2021-10-03 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_competitions_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='length',
        ),
    ]
