import re
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from .models import Profile, Post, Community, CommunityMembership, DiscussionPod
 
 
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
def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Post.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(body__icontains=query) |
            models.Q(category__icontains=query)
        ).select_related('user')
    return render(request, 'proj1App/search.html', {'results': results, 'query': query})

@login_required
def create_post(request):
    if request.method == 'POST':
        title    = request.POST.get('title', '')
        body     = request.POST.get('body', '')
        category = request.POST.get('category', 'General')
        link     = request.POST.get('link', '')
        image    = request.FILES.get('image')
        pdf      = request.FILES.get('pdf')
        next_url = request.POST.get('next', '/home/')
 
        if not any([title, body, image, pdf, link]):
            return redirect(next_url)
        
        hashtags = re.findall(r'#(\w+)', body.lower())
        community = None
        for tag in hashtags:
            match = Community.objects.filter(slug=tag).first()
            if match:
                community = match
                break
 
        Post.objects.create(
            user=request.user, title=title, body=body,
            category=category, link=link, image=image, pdf=pdf,
            community=community
        )
        return redirect(next_url)
 
    return redirect('/home/')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    next_url = request.POST.get('next', '/home/')
    if request.method == 'POST':
        post.delete()
        return redirect(next_url)
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

@login_required
def join_community(request, community_slug):
    community = get_object_or_404(Community, slug=community_slug)
    CommunityMembership.objects.get_or_create(user=request.user, community=community)
    return redirect(request.POST.get('next', '/communities/'))

@login_required
def leave_community(request, community_slug):
    community = get_object_or_404(Community, slug=community_slug)
    CommunityMembership.objects.filter(user=request.user, community=community).delete()
    return redirect(request.POST.get('next', '/communities/'))

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')

        if bio is not None:
            profile.bio = bio

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile')

    recent_notes = Post.objects.filter(user=request.user)[:6]

    return render(request, 'proj1App/profile.html', {
        'profile': profile,
        'recent_notes': recent_notes,
    })

@login_required
def settings(request): 
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':

        # handling for the deleting account 
        if request.POST.get('delete_account') == 'true': 
            request.user.delete()
            return redirect('index') 
        
        # this handles the password change in settings
        new_password = request.POST.get('new_password', '')
        if new_password: 
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')  # log the user back in with new password

        # this handles the username change
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'That username is already taken.')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username updated.')


    return render(request, 'proj1App/settings.html', {'profile': profile})