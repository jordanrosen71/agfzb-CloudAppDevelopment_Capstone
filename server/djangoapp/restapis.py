import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url)

    # If the response is a dictionary and contains the "rows" key
    if isinstance(json_result, dict) and "rows" in json_result:
        dealers = json_result["rows"]
    elif isinstance(json_result, list):  # If the response is a list
        dealers = json_result
    else:
        raise ValueError("Unexpected structure of the response data")

    # For each dealer object
    for dealer in dealers:
        # If the dealer is a dictionary and has the "doc" key
        if isinstance(dealer, dict) and "doc" in dealer:
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], 
                                   full_name=dealer_doc["full_name"], id=dealer_doc["id"], 
                                   lat=dealer_doc["lat"], long=dealer_doc["long"], 
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], 
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []

    # Add dealerId to kwargs
    kwargs = {"dealerId": dealerId}

    # Call get_request with a URL parameter and dealerId
    json_result = get_request(url, **kwargs)

    # If the response is a dictionary and contains the "rows" key
    if isinstance(json_result, dict) and "rows" in json_result:
        reviews = json_result["rows"]
    elif isinstance(json_result, list):  # If the response is a list
        reviews = json_result
    else:
        raise ValueError("Unexpected structure of the response data")

    # For each review object
    for review in reviews:
        # If the review is a dictionary and has the "doc" key
        if isinstance(review, dict) and "doc" in review:
            review_doc = review["doc"]
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealer_id=review_doc["dealership"], review=review_doc["review"], 
                                      reviewer_name=review_doc["name"], purchase=review_doc["purchase"], 
                                      purchase_date=review_doc.get("purchase_date", None), 
                                      car_make=review_doc.get("car_make", None), 
                                      car_model=review_doc.get("car_model", None))
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



