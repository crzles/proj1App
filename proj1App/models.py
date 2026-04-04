from django.db import models
from django.contrib.auth.models import User

# Create your models here; a table in your database

# profile model - for now they will be in comments
# from django.contrib.auth.models import User 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    