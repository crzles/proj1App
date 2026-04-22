from django.shortcuts import render, redirect  #render/show HTML page, redirect/send user to another URL
from .forms import PostForm  #import the form from forms.py

# Create your views here.

def create_post(request):  #this function handles the "create post" page
    if request.method == 'POST':  #checks if the user submitted the form (clicked submit button)

        form = PostForm(request.POST, request.FILES)
        #request.POST = text data from form (title, content, etc.)
        #request.FILES = uploaded files (images, PDFs, etc.)

        if form.is_valid():  #checking if all data is correct (required fields, valid file, etc.)
            form.save()  #saves the form data into the database (creates a Post object)
            return redirect('create_post')  #sends user back to the same page (prevents resubmission)

    else:
        form = PostForm()  #if user is just opening the page, show an empty form

    return render(request, 'create_post.html', {'form': form})
    #render = displays the HTML template
    #'create_post.html' = the page shown to the user
    #{'form': form} = sends the form into the HTML so it can display it