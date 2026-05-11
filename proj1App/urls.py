# url for home page

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
