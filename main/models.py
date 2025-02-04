from django.db import models

# Create your models here.


class competitions(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    submissions = models.IntegerField()
    lang = models.CharField(max_length=50)
    date = models.DateField(auto_now=False)
    result = models.BooleanField(default=False)


class submissions(models.Model):
    pgid = models.IntegerField()
    submitted_by = models.CharField(max_length=50)
    sub_date = models.DateField(auto_now=True)
    sub_time = models.TimeField(auto_now=True)
    code = models.TextField()


class resultmodel(models.Model):
    position = models.IntegerField()
    username = models.TextField()
    comp_id = models.IntegerField()
    sub_id = models.IntegerField()


class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()
