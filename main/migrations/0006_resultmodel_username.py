# Generated by Django 3.2.7 on 2021-10-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_resultmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultmodel',
            name='username',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]