# url for home page

from django.urls import path

urlpatterns = [
    path('', views.home, name ='home'),
]