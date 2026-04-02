from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

# Create your views here.
#python functinos that take http requests and return http response like html documents
 
def index(request):
    context ={}
    template = loader.get_template("index.html");
    return HttpResponse(template.render(context, request));

def login(request):
    email = request.GET["email"]
    password = request.GET["password"]
    context={"useremail": email}
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request));
