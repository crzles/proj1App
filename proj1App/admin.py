from django.contrib import admin
from .models import Profile

# Register your models here; able to see database in django admin
#python manage.py runserver
#go to website and login
admin.site.register(Profile)