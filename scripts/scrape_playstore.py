#!/usr/bin/env python3
"""
Script to scrape Play Store details for all apps listed in otherApps.json
Saves the details in {fileId}.json files in the appPlaystoreDetail folder
"""

import json
import os
import sys
from pathlib import Path
from google_play_scraper import app, exceptions

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Paths
OTHER_APPS_JSON = PROJECT_ROOT / "api" / "otherApps.json"
OUTPUT_DIR = PROJECT_ROOT / "api" / "appPlaystoreDetail"

def ensure_output_dir():
    """Ensure the output directory exists"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def load_app_ids():
    """Load the app IDs from otherApps.json"""
    try:
        with open(OTHER_APPS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('ids', {})
    except FileNotFoundError:
        print(f"Error: {OTHER_APPS_JSON} not found!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {OTHER_APPS_JSON}: {e}")
        sys.exit(1)

def scrape_app_details(package_name, file_id):
    """Scrape all available details for an app from Play Store"""
    try:
        print(f"\nScraping {package_name} (ID: {file_id})...")
        
        # Fetch app details with all available information
        result = app(
            package_name,
            lang='en',  # Language
            country='us'  # Country
        )
        
        # The result contains all available fields:
        # - title, description, descriptionHTML
        # - summary, installs, minInstalls, score, ratings, reviews
        # - price, free, currency, offersIAP
        # - size, androidVersion, androidVersionText
        # - developer, developerId, developerEmail, developerAddress, developerWebsite
        # - privacyPolicy, genre, genreId, icon, headerImage
        # - screenshots, video, videoImage, contentRating
        # - adSupported, released, updated, version, recentChanges
        # - comments, similarApps, moreByDeveloper, etc.
        
        return result
        
    except exceptions.NotFoundError:
        print(f"  ⚠️  App {package_name} not found on Play Store")
        return None
    except exceptions.NetworkError as e:
        print(f"  ⚠️  Network error for {package_name}: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Error scraping {package_name}: {e}")
        return None

def save_app_details(details, file_id):
    """Save app details to a JSON file"""
    if details is None:
        print(f"  ⚠️  Skipping save for ID {file_id} (no details available)")
        return False
    
    output_file = OUTPUT_DIR / f"{file_id}.json"
    
    try:
        # Convert the result to a dictionary and save as pretty JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(details, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"  ✅ Saved to {output_file}")
        return True
    except Exception as e:
        print(f"  ⚠️  Error saving to {output_file}: {e}")
        return False

def main():
    """Main function to orchestrate the scraping"""
    print("=" * 60)
    print("Play Store Scraper")
    print("=" * 60)
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Load app IDs
    app_ids = load_app_ids()
    print(f"\nFound {len(app_ids)} apps to scrape")
    
    # Statistics
    successful = 0
    failed = 0
    
    # Scrape each app
    for package_name, file_id in app_ids.items():
        details = scrape_app_details(package_name, file_id)
        
        if details:
            if save_app_details(details, file_id):
                successful += 1
            else:
                failed += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Scraping Summary")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"⚠️  Failed: {failed}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
