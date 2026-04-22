from django.db import models

class Post(models.Model):
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    topic = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)