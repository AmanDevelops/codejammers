# Generated by Django 3.2.7 on 2021-10-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_submissions_sub_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='resultmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('comp_id', models.IntegerField()),
                ('sub_id', models.IntegerField()),
            ],
        ),
    ]
