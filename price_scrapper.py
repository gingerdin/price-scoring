import requests
import json
import os
from datetime import datetime

def fetch_game_data(app_id):
    """Fetch game data from Steam API"""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    
    try:
        print(f"\nMaking request to: {url}\n")
        response = requests.get(url)
        response.raise_for_status()
        
        print(f"Status code: {response.status_code}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_game_data(data, app_id):
    """Save game data to a JSON file"""
    filename = f"{app_id}_price.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved data to {filename}")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def main():
    # List of app IDs to fetch
    app_ids = [
        "2951990",
          "912833"  # Replace with your app IDs
        # Add more app IDs as needed
    ]
    
    for app_id in app_ids:
        print(f"\nFetching data for app ID: {app_id}")
        data = fetch_game_data(app_id)
        
        if data:
            save_game_data(data, app_id)

if __name__ == "__main__":
    import sys
    app_id = sys.argv[1] if len(sys.argv) > 1 else "2951990"
    data = fetch_game_data(app_id)
    if data:
        save_game_data(data, app_id)
