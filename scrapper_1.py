import requests
import time
import json

def fetch_reviews(app_id, max_pages=5):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    params = {
        "filter": "recent",
        "language": "english",
        "review_type": "all",
        "purchase_type": "all",
        "cursor": "*",
    }
    
    reviews = []
    for page in range(max_pages):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            if "reviews" in data:
                reviews.extend(data["reviews"])
                print(f"Fetched page {page + 1}: {len(data['reviews'])} reviews...")
            else:
                print(f"No reviews found in response: {data}")
                break
            
            # Update the cursor for pagination
            params["cursor"] = data.get("cursor", "")
            if params["cursor"]:
                params["cursor"] = params["cursor"].replace("+", "%2B")  # Ensure the cursor is URL-safe
            else:
                print("No more pages to fetch")
                break
            
            if not data.get("success", 0) or not data["reviews"]:
                print("No more reviews available")
                break
            
            # Pause to avoid rate-limiting
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            break
    
    return reviews

# Fetch reviews for Palworld (app ID: 2574900)
app_id = "2574900"
all_reviews = fetch_reviews(app_id, max_pages=3)

# Print a few sample reviews
print(f"\nTotal reviews fetched: {len(all_reviews)}")
if all_reviews:
    print("\nSample reviews:")
    for i, review in enumerate(all_reviews[:5], 1):
        print(f"\nReview #{i}:")
        print("Review:", review["review"])
        print("Recommended:", review["voted_up"])
        print("Helpful:", review["votes_up"], "times")