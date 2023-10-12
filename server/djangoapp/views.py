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
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_dealer_review_to_cf

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
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ae0b8375-fe14-4488-a0ce-31d937867378/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/ae0b8375-fe14-4488-a0ce-31d937867378/dealership-package/get-review?dealership={dealer_id}"
        
        # Get the reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        # Construct a response by aggregating all the review information
        response_content = ""
        for review in reviews:
            # Assuming your DealerReview object has a __str__ method to represent itself
            response_content += str(review) + "\n"
        
        return HttpResponse(response_content)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        # Display form...
        print('Form displayed here')
    elif request.method == "POST":
        # Extract form data
        # review_data = {
        #     "name": request.POST.get("name"),
        #     "dealership": dealer_id,
        #     "review": request.POST.get("review"),
        #     "purchase": request.POST.get("purchase") == "true",
        #     "purchase_date": request.POST.get("purchase_date"),
        #     "car_make": request.POST.get("car_make"),
        #     "car_model": request.POST.get("car_model"),
        #     "car_year": int(request.POST.get("car_year"))
        # }
        review_data = {
            "name": "John Doe",
            "dealership": "123456",
            "review": "Great dealership, friendly staff and excellent service.",
            "purchase": "true",
            "purchase_date": "2023-10-10",
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2023
        }

        # Construct the data to be sent to the API
        review_data_payload = {
            "action": "postReview",
            "reviewData": review_data
        }

        # Endpoint to post the review
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ae0b8375-fe14-4488-a0ce-31d937867378/dealership-package/post-review"
        
        # Use the post_dealer_review_to_cf function
        api_response = post_dealer_review_to_cf(url, review_data_payload)

        # Redirect to the dealer details page or show error
        if api_response:
            return HttpResponseRedirect(f'/djangoapp/dealer/{dealer_id}/')  # Assuming this is the URL pattern for dealer details
        else:
            return HttpResponse(f"<p>error</p>")
