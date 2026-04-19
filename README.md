# Seaboy

Seaboy — Sentinel-2 Satellite Imagery Fetcher
A Python toolkit for authenticating with the Copernicus Data Space Ecosystem (CDSE) and downloading Sentinel-2 satellite imagery via the Sentinel Hub Processing API.

Overview
Seaboy fetches true-colour (RGB) Sentinel-2 L2A satellite images for a defined geographic area and saves them as GeoTIFF files. It also includes utilities to test your CDSE connection and visualise downloaded imagery with contrast enhancement.
The default area of interest is the San Francisco Bay Area, but the bounding box can be changed to any location.

Prerequisites

Python 3.9+
A Copernicus Data Space Ecosystem (CDSE) account
Your CDSE OAuth2 Client ID and Client Secret (generated in the CDSE dashboard)

Usage
Test your connection
Verify that your credentials are valid and the CDSE endpoints are reachable:
bashpython scripts/test_connection.py
Download a Sentinel-2 image
Fetches a true-colour GeoTIFF for the configured area and time range and saves it to data/:
bashpython scripts/fetch_sentinel_image.py
By default this downloads imagery for the San Francisco Bay Area from a 5-day window ending 1 March 2024, filtered to scenes with less than 80% cloud cover.
View a downloaded image
Opens a matplotlib window showing the raw and contrast-enhanced versions of the most recently downloaded image:
bashpython scripts/view_image.py
Debug OAuth2 authentication
Prints your resolved environment variables and attempts a raw token request — useful for diagnosing credential issues:
bashpython scripts/auth_test.py

Configuration
The src/config_sentinel.py module is the central configuration object used across all scripts. It:

Reads credentials from .env
Points all requests at the CDSE Sentinel Hub endpoints
Automatically fetches and stores an OAuth2 bearer token at import time

To change the area of interest, edit the bbox_coords list in fetch_sentinel_image.py:
pythonbbox_coords = [-122.45, 37.77, -122.35, 37.87]  # [min_lon, min_lat, max_lon, max_lat]
To change the date range, edit end_date and the timedelta:
pythonend_date = datetime(2024, 3, 1, 12, 0)
start_date = end_date - timedelta(days=5)

Output
Downloaded images are saved to the data/ directory as GeoTIFF files:
data/sentinel_image_YYYYMMDD.tiff
The data/ directory is git-ignored to avoid committing large binary files.

Dependencies
Key packages (see requirements.txt for pinned versions):
PackagePurposesentinelhubSentinel Hub SDK and request helpersrasterioReading and writing GeoTIFF filesnumpyArray operations and image scalingmatplotlibImage visualisationgeopandas / shapelyGeospatial data handlingpython-dotenvLoading credentials from .envrequestsDirect HTTP calls to the Processing API

Notes

The Sentinel-2 evalscript scales band values from the native 0–10,000 DN range down to 0–255 RGB for display. Adjust the scale constant in fetch_sentinel_image.py to control image brightness.
Imagery resolution is set to 10 metres per pixel, which is the native resolution of Sentinel-2 visible bands.
Cloud filtering uses mosaickingOrder: leastCC (least cloud coverage first).
