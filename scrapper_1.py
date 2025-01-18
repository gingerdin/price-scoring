import requests
import time
import json
import os
import csv
from urllib.parse import quote

def fetch_reviews(app_id, max_pages=5):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    params = {
        "filter": "recent",
        "language": "english",
        "review_type": "all",
        "purchase_type": "all",
        "num_per_page": 100,
        "cursor": "*",
    }
    
    reviews = []
    current_page = 0
    query_summary = None  # Store query summary from first request
    
    try:
        while True:  # Continue until we break due to empty cursor
            data = make_request(url, params)
            
            # Store query summary from first request
            if current_page == 0:
                query_summary = data.get('query_summary', {})
                print(f"Query summary: {query_summary}")
            
            if "reviews" in data and len(data["reviews"]) > 0:
                reviews.extend(data["reviews"])
                current_page += 1
                print(f"Fetched page {current_page}: {len(data['reviews'])} reviews...")
            else:
                print(f"No reviews found in response: {data}")
                break
            
            next_cursor = data.get("cursor", "")
            if not next_cursor:
                print("No more pages to fetch - cursor is empty")
                break
            
            print(f"\nNext cursor value: {next_cursor}")
            params["cursor"] = next_cursor.replace("+", "%2B")  # Ensure the cursor is URL-safe
            print(f"URL-encoded cursor: {params['cursor']}\n")
            
            if not data.get("success", 0):
                print("No more reviews available")
                break
            
            # Pause to avoid rate-limiting
            time.sleep(1)
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reviews: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
    
    return reviews, query_summary

def make_request(url, params):
    # Prepare the URL without decoding '=' symbols
    param_strings = []
    for key, value in params.items():
        param_strings.append(f"{key}={value}")
    full_url = f"{url}&{'&'.join(param_strings)}"
    
    print(f"\nMaking request to: {full_url}\n")

    response = requests.get(full_url)
    response.raise_for_status()
    data = response.json()

    # print(f"Response: {data}")
    print(response.status_code)
    print(f"Response cursor: {data.get('cursor', 'None')}")

    return data


def save_reviews(reviews, app_id, query_summary, filename='data_2.json'):
    """Save reviews to a JSON file. If file exists, append new reviews."""
    try:
        # Create the data structure
        review_data = {
            'app_id': app_id,
            'total_reviews': len(reviews),
            'query_summary': query_summary,  # Add query summary to the data
            'reviews': reviews
        }
        
        if os.path.exists(filename):
            # If file exists, load existing data and append new reviews
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Check if we already have reviews for this app_id
                if str(app_id) in existing_data:
                    # Add only new reviews (avoid duplicates)
                    existing_reviews = set(r['recommendationid'] for r in existing_data[str(app_id)]['reviews'])
                    new_reviews = [r for r in reviews if r['recommendationid'] not in existing_reviews]
                    
                    existing_data[str(app_id)]['reviews'].extend(new_reviews)
                    existing_data[str(app_id)]['total_reviews'] = len(existing_data[str(app_id)]['reviews'])
                    existing_data[str(app_id)]['query_summary'] = query_summary  # Update query summary
                    print(f"Added {len(new_reviews)} new reviews to existing data")
                else:
                    # Add new app_id data
                    existing_data[str(app_id)] = review_data
                    print(f"Added new app_id {app_id} with {len(reviews)} reviews")
                
                # Save updated data
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                
            except json.JSONDecodeError:
                print(f"Error reading existing file. Creating new file.")
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({str(app_id): review_data}, f, indent=2, ensure_ascii=False)
        else:
            # Create new file with the reviews
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({str(app_id): review_data}, f, indent=2, ensure_ascii=False)
            print(f"Created new file with {len(reviews)} reviews")
            
    except Exception as e:
        print(f"Error saving reviews: {e}")
        return False
    
    return True

def save_reviews_csv(reviews, app_id, query_summary, filename='data_2.csv'):
    """Save reviews to a CSV file with relevant fields and query summary."""
    try:
        # Define the fields we want to save
        fields = [
            'recommendationid',
            'author.steamid',
            'author.playtime_forever',
            'author.playtime_at_review',
            'language',
            'review',
            'timestamp_created',
            'timestamp_updated',
            'voted_up',
            'votes_up',
            'votes_funny',
            'weighted_vote_score',
            'comment_count',
            'steam_purchase',
            'received_for_free'
        ]

        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(filename)
        print(f"Filename: {filename}")
        
        mode = 'a' if file_exists else 'w'
        with open(filename, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers and query summary if new file
            if not file_exists:
                # Write query summary as metadata rows
                writer.writerow(['# Query Summary'])
                for key, value in query_summary.items():
                    writer.writerow([f'# {key}', value])
                writer.writerow([])  # Empty row for separation
                
                # Write data headers
                writer.writerow(['app_id'] + fields)
            
            # Write review data
            for review in reviews:
                row = [app_id]
                for field in fields:
                    if '.' in field:
                        # Handle nested fields like author.steamid
                        main_key, sub_key = field.split('.')
                        value = review.get(main_key, {}).get(sub_key, '')
                    else:
                        value = review.get(field, '')
                    row.append(value)
                writer.writerow(row)
                
        print(f"Successfully saved {len(reviews)} reviews to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving reviews to CSV: {e}")
        return False

# Fetch reviews for Palworld (app ID: 2574900)
app_id = "1670540"
all_reviews, query_summary = fetch_reviews(app_id, max_pages=0)

# Save the reviews to both JSON and CSV files
if __name__ == "__main__":
    import sys
    app_id = sys.argv[1] if len(sys.argv) > 1 else "1670540"
    all_reviews, query_summary = fetch_reviews(app_id, max_pages=0)
    
    if all_reviews:
        print(f"\nTotal reviews fetched: {len(all_reviews)}")
        
        json_filename = f"{app_id}_reviews.json"
        if save_reviews(all_reviews, app_id, query_summary, json_filename):
            print(f"Successfully saved reviews to {json_filename}")
        else:
            print("Failed to save reviews to JSON")
            
        csv_filename = f"{app_id}_reviews.csv"
        if save_reviews_csv(all_reviews, app_id, query_summary, csv_filename):
            print(f"Successfully saved reviews to {csv_filename}")
        else:
            print("Failed to save reviews to CSV")

    # Print sample of reviews
    # print("\nSample reviews:")
    # for i, review in enumerate(all_reviews[:5], 1):
    #     print(f"\nReview #{i}:")
    #     print("Review:", review["review"])
    #     print("Recommended:", review["voted_up"])
    #     print("Helpful:", review["votes_up"], "times")