from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')  # Assuming 'index' is the name of your homepage view
        else:
            context["error"] = "Invalid username or password."

    return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')  # Redirect to the homepage after logging out

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']

        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            # Ideally, send a message to the user saying the username already exists
            return render(request, 'djangoapp/registration.html', {'error': 'Username already exists!'})
        else:
            # Create a new user and save them to the database
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Log the user in (optional)
            login(request, user)

            # Redirect to homepage after successful registration (or any other page you want)
            return redirect('djangoapp:index')

    else:
        # If it's a GET request, just render the registration page
        return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

