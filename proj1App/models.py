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

    #tie a post to a community
    community  = models.ForeignKey(
        'Community', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts'
    )

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.created_at:%Y-%m-%d}"
    
class Community(models.Model):
    name    = models.CharField(max_length=100, unique=True)   # e.g. "computerscience"
    slug    = models.SlugField(max_length=100, unique=True)    # used in URLs
    members = models.ManyToManyField(
        User, through='CommunityMembership', related_name='communities', blank=True
)

    # popular topics are just sub-communities (child communities)
    parent  = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='subcommunities'
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'communities'

    def __str__(self):
        return f"#{self.name}"

    @property
    def member_count(self):
        return self.members.count()

    @property
    def post_count(self):
        return self.posts.count()


class CommunityMembership(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f"{self.user.username} → #{self.community.name}"


class DiscussionPod(models.Model):
    community    = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='pods')
    name         = models.CharField(max_length=60)          # e.g. "Pod A"
    participants = models.ManyToManyField(User, blank=True, related_name='active_pods')
    is_active    = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.community} — {self.name}"

    @property
    def participant_count(self):
        return self.participants.count()