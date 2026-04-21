from django.shortcuts import render

# View for the home page
def home(request):
    return render(request, 'proj1App/home.html')