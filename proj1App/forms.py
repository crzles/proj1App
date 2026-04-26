from django import forms #import forms system (user input, validation,etc)
from .models import Post #importing my post model as a blueprint

class PostForm(forms.ModelForm): #class 
    class Meta: #config. for form
        model = Post
        fields = ['title', 'content', 'topic', 'is_public', 'file']