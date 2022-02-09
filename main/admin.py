from django.contrib import admin
from .models import competitions, resultmodel, submissions
# Register your models here.

admin.site.register(competitions)
admin.site.register(submissions)
admin.site.register(resultmodel)
