import subprocess
import sys
import time

def run_scrappers(app_ids):
    """Run both price and review scrappers for given app IDs"""
    for app_id in app_ids:
        print(f"\n{'='*50}")
        print(f"Processing app ID: {app_id}")
        print(f"{'='*50}\n")
        
        try:
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
    # List of app IDs to process
    app_ids = [
        "2951990",
          "912833"   # Example app ID
        # Add more app IDs as needed
    ]
    
    print(f"Starting to process {len(app_ids)} app(s)")
    run_scrappers(app_ids)
    print("\nAll processing completed!")

if __name__ == "__main__":
    main() 