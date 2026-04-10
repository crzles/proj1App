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
    

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Biology', 'Biology'),
        ('Chemistry', 'Chemistry'),
        ('Business', 'Business'),
        ('General', 'General'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category   = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='General')
    title      = models.CharField(max_length=200, blank=True)
    body       = models.TextField(blank=True)
    image      = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    pdf        = models.FileField(upload_to='posts/pdfs/', blank=True, null=True)
    link       = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.created_at:%Y-%m-%d}"