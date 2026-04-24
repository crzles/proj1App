from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post, Community, DiscussionPod
 
 
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'proj1App/index.html')
 
 
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
 
        if User.objects.filter(username=username).exists():
            messages.error(request, 'An account with that username already exists.')
            return redirect('signup')
 
        user = User.objects.create_user(username=username, email=username, password=password)
        Profile.objects.create(user=user)
        auth_login(request, user)
        return redirect('home')
 
    return render(request, 'proj1App/signup.html')
 
 
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
 
    return render(request, 'proj1App/login.html')
 
 
@login_required
def home(request):
    posts = Post.objects.all().select_related('user')
    return render(request, 'proj1App/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title    = request.POST.get('title', '')
        body     = request.POST.get('body', '')
        category = request.POST.get('category', 'General')
        link     = request.POST.get('link', '')
        image    = request.FILES.get('image')
        pdf      = request.FILES.get('pdf')
 
        if not any([title, body, image, pdf, link]):
            posts = Post.objects.all().select_related('user')
            return render(request, 'proj1App/home.html', {
                'posts': posts,
                'error': 'Post must have at least some content.'
            })
 
        Post.objects.create(
            user=request.user, title=title, body=body,
            category=category, link=link, image=image, pdf=pdf,
        )
        return redirect('/home/')
 
    return redirect('/home/')


@login_required
def communities(request, community_slug=None):
    # Communities the logged-in user has joined
    user_communities = request.user.communities.filter(parent=None).prefetch_related('subcommunities')
 
    # Which community is currently active (defaults to first one)
    if community_slug:
        current_community = get_object_or_404(Community, slug=community_slug)
    elif user_communities.exists():
        current_community = user_communities.first()
    else:
        current_community = None
 
    # Popular topics = top 5 sub-communities by post count
    popular_topics = (
        Community.objects.filter(parent=current_community)
        .annotate_post_count()  # see note below — replace with the line below if you haven't added annotations
        if current_community else Community.objects.none()
    )
    # Simpler version without annotation (use this one):
    popular_topics = (
        Community.objects.filter(parent=current_community)
        if current_community else Community.objects.none()
    )
 
    # Discover = communities the user hasn't joined yet
    joined_ids = request.user.communities.values_list('id', flat=True)
    discover_communities = (
        Community.objects.filter(parent=None)
        .exclude(id__in=joined_ids)[:8]
    )
 
    # Recent posts in the current community
    recent_posts = (
        Post.objects.filter(community=current_community)
        .select_related('user')
        if current_community else Post.objects.none()
    )
 
    # Discussion pods for the current community
    discussion_pods = (
        DiscussionPod.objects.filter(community=current_community)
        .prefetch_related('participants')
        if current_community else DiscussionPod.objects.none()
    )
 
    return render(request, 'proj1App/communities.html', {
        'user_communities':     user_communities,
        'current_community':    current_community,
        'popular_topics':       popular_topics,
        'discover_communities': discover_communities,
        'recent_posts':         recent_posts,
        'discussion_pods':      discussion_pods,
    })

def logout(request):
    auth_logout(request)
    return redirect('login')
