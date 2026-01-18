# Play Store Scraper

This script scrapes detailed information from the Google Play Store for all apps listed in `api/otherApps.json`.

## Setup

1. Install the required Python package:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install google-play-scraper
```

## Usage

Run the script from the project root:

```bash
python scripts/scrape_playstore.py
```

Or from the scripts directory:

```bash
cd scripts
python scrape_playstore.py
```

## Output

The script will:
- Read package names and IDs from `api/otherApps.json`
- Scrape all available details from Play Store for each app
- Save the details in `api/appPlaystoreDetail/{fileId}.json` files

For example:
- `com.mobileappzgroup.lovelines` → `api/appPlaystoreDetail/1.json`
- `com.mobileappzgroup.inspireme` → `api/appPlaystoreDetail/2.json`
- etc.

## Data Retrieved

The script fetches all available Play Store information including:
- App title, description, summary
- Ratings, reviews, install count
- Price, size, Android version requirements
- Developer information
- Screenshots, videos, icons
- Content rating, genre
- Recent changes, version info
- And more...
