from django.db import models 
#importing model system

class Post(models.Model):  #creating database table 
    content = models.TextField()  #creates column that stores text
    is_public = models.BooleanField(default=True) #true -> public and false private
    topic = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', null=True, blank=True) #file uploads
    created_at = models.DateTimeField(auto_now_add=True) #storing time and date of post