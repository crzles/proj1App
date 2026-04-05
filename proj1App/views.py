from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile #importing profile class from models.py

# Create your views here.
#python functions that take http requests and return http response like html documents

#def function(object passing each URL visit)
def index(request):
    if request.user.is_authenticated: #did user alr logged in
        return redirect('home') #if yes then redirect
    return render(request, 'index.html') #render: sends back an HTML page

def signup(request):
    if request.method == 'POST': #POST: user submitted form, GET: user just visited page
        username = request.POST['username'] #reads value inserted by user like cin
        password = request.POST['password']

        if User.objects.filter(username=username).exists(): #if it exists in database
            messages.error(request, 'An account with that email already exists.') #storing error mssg, displayed in HTML via {% if messages %}
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=username, password=password)
        Profile.objects.create(user=user)
        auth_login(request, user)
        return redirect('home')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        
    return render(request, 'login.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('login')