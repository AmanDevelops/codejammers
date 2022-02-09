# Generated by Django 3.2.7 on 2021-10-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='submissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_by', models.CharField(max_length=50)),
                ('length', models.IntegerField()),
                ('sub_date', models.DateField(auto_now=True)),
                ('code', models.TextField()),
            ],
        ),
    ]