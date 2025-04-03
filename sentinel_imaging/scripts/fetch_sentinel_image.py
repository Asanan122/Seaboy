from sentinelhub import (
    SentinelHubRequest, 
    DataCollection, 
    BBox, 
    bbox_to_dimensions, 
    MimeType,
    CRS
)
from datetime import datetime, timedelta
import os
from pathlib import Path
import requests
from src.config_sentinel import sentinel_config

def fetch_sentinel_image():
    """Fetch and save a Sentinel-2 image."""
    
    # Use the global configuration
    config = sentinel_config
    
    # Verify configuration
    print(f"🔍 DEBUG - Verifying CDSE Configuration:")
    print(f"  - BASE_URL: {config.sh_base_url}")
    print(f"  - PROCESS_URL: {config.processing_api_url}")
    print(f"  - TOKEN: {config.oauth_token[:30]}...")

    # Define bounding box (San Francisco Bay Area)
    bbox_coords = [-122.45, 37.77, -122.35, 37.87]
    bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
    bbox_size = bbox_to_dimensions(bbox, resolution=10)

    # Use specific dates with proper ISO format
    end_date = datetime(2024, 3, 1, 12, 0)  # Use noon UTC
    start_date = end_date - timedelta(days=5)
    
    # Format dates in ISO-8601 format
    time_interval = (
        start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    print(f"📅 Time interval: {time_interval[0]} to {time_interval[1]}")
    print(f"📍 Bounding box coordinates: {bbox_coords}")
    print(f"🎯 Image dimensions: {bbox_size}")

    # Create direct process API request
    process_request = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                },
                "bbox": bbox_coords
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": time_interval[0],
                        "to": time_interval[1]
                    },
                    "mosaickingOrder": "leastCC",
                    "maxCloudCoverage": 80
                }
            }]
        },
        "output": {
            "width": bbox_size[0],
            "height": bbox_size[1],
            "responses": [{
                "identifier": "default",
                "format": {
                    "type": "image/tiff"
                }
            }]
        },
        "evalscript": """
            //VERSION=3
            function setup() {
                return {
                    input: [{
                        bands: ["B04", "B03", "B02"],
                        units: "DN"
                    }],
                    output: {
                        bands: 3,
                        sampleType: "UINT8"
                    }
                };
            }

            function evaluatePixel(sample) {
                // Sentinel-2 data comes in 0-10000 range
                // We need to scale it to 0-255 for RGB display
                const scale = 255 / 2000;  // Adjust denominator to control brightness
                
                return [
                    Math.min(255, Math.max(0, sample.B04 * scale)),
                    Math.min(255, Math.max(0, sample.B03 * scale)),
                    Math.min(255, Math.max(0, sample.B02 * scale))
                ];
            }
        """
    }

    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Execute request directly using process API
    try:
        print("🔄 Attempting to download images...")
        print(f"  Request URL: {config.processing_api_url}")
        print(f"  Time range: {time_interval[0]} to {time_interval[1]}")
        
        response = requests.post(
            config.processing_api_url,
            headers={
                'Authorization': f'Bearer {config.oauth_token}',
                'Content-Type': 'application/json'
            },
            json=process_request
        )
        response.raise_for_status()
        
        # Save the image
        filename = data_dir / f"sentinel_image_{start_date.strftime('%Y%m%d')}.tiff"
        filename.write_bytes(response.content)
        print(f"✅ Image saved to: {filename}")
            
    except Exception as e:
        print(f"❌ Error downloading images:")
        print(f"  - Error type: {type(e).__name__}")
        print(f"  - Error message: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  - Response: {e.response.text}")

if __name__ == "__main__":
    fetch_sentinel_image()