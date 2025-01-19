import subprocess
import sys
import time
import requests
import json

def get_app_type(app_id):
    """Get app type from Steam API"""
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=basic"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data and data.get(str(app_id), {}).get('success'):
            app_data = data[str(app_id)]['data']
            return app_data.get('type', '').lower()
            
        return None
        
    except Exception as e:
        print(f"Error fetching app type for {app_id}: {e}")
        return None

def load_app_ids(filename="strategy_progress.json"):
    """Load app IDs from strategy progress file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return [str(game['appid']) for game in data.get('found_games', [])]
    except Exception as e:
        print(f"Error loading app IDs from {filename}: {e}")
        return []

def run_scrappers(app_ids):
    """Run both price and review scrappers for given app IDs"""
    for app_id in app_ids:
        print(f"\n{'='*50}")
        print(f"Processing app ID: {app_id}")
        print(f"{'='*50}\n")
        
        try:
            # Check if app is DLC first
            app_type = get_app_type(app_id)
            if app_type != 'dlc':
                print(f"Skipping {app_id} - not a DLC (type: {app_type})")
                continue
                
            print(f"Confirmed DLC, proceeding with scraping...")
            
            # Run price scrapper
            print("\nRunning price scrapper...")
            subprocess.run([sys.executable, "price_scrapper.py", app_id], check=True)
            
            # Wait a bit between requests
            time.sleep(2)
            
            # Run review scrapper
            print("\nRunning review scrapper...")
            subprocess.run([sys.executable, "scrapper_1.py", app_id], check=True)
            
            print(f"\nSuccessfully processed app ID: {app_id}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing app ID {app_id}: {e}")
        except Exception as e:
            print(f"Unexpected error for app ID {app_id}: {e}")
        
        # Wait between processing different apps
        time.sleep(5)

def main():
    # Load app IDs from strategy_progress.json
    # app_ids = load_app_ids()
    app_ids = [
        "2891710",
        "2891700",
        "2325832",
        "2059190",
        "1834066",
        "1834065",
        "1834064",
        "1834063",
        "1834062",
        "1834061",
        "1834060",
        "1834058",
        "1834057",
        "1834056",
        "1834055",
        "1834054",
        "1834053",
        "1834052",
        "1834051",
        "1834050",
        "1834049",
        "1834048",
        "1834047",
        "1834046",
        "1834045",
        "1834044",
        "1834043",
        "1834042",
        "1834041",
        "1834040",
        "1834039",
        "1834038",
        "1834037",
        "1834036",
        "1834035",
        "1834034",
        "1834033",
        "1834032",
        "1834031",
        "1834030",
        "1834027",
        "1834026",
        "1834025",
        "1834024",
        "1834023",
        "1834022",
        "1834021",
        "1834020",
        "1824060",
        "1374300",
    ]
    
    if not app_ids:
        print("No app IDs found in strategy_progress.json")
        return
    
    print(f"Starting to process {len(app_ids)} app(s)")
    run_scrappers(app_ids)
    print("\nAll processing completed!")

if __name__ == "__main__":
    main() 