from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Any other fields can be added as needed

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        # Add more types as needed
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer_id = models.PositiveIntegerField()
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    year = models.DateField(default=now)
    # Any other fields can be added as needed

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealer_id, review, reviewer_name, purchase, purchase_date=None, car_make=None, car_model=None, rating=None):
        # Dealer ID (associated with the reviewed dealer)
        self.dealer_id = dealer_id

        # The content of the review
        self.review = review

        # The name of the reviewer
        self.reviewer_name = reviewer_name

        # Boolean to indicate if the reviewer made a purchase from the dealer
        self.purchase = purchase

        # If a purchase was made, the date of the purchase
        self.purchase_date = purchase_date

        # If a purchase was made, the make of the car
        self.car_make = car_make

        # If a purchase was made, the model of the car
        self.car_model = car_model

        # Overall rating given by the reviewer
        self.rating = rating

    def __str__(self):
        return f"Review by {self.reviewer_name} for Dealer ID {self.dealer_id}: {self.review}"

