import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sentinelhub import SentinelHubRequest, DataCollection, BBox, bbox_to_dimensions, MimeType
from src.config_sentinel import get_sentinelhub_config



def fetch_sentinel_image():
    # 1. Grab the config from the .env file
    config = get_sentinelhub_config()

    # 2. Define a small area of interest (bounding box).
    # Example coordinates for a coastal area (update as needed)
    bbox_coords = [-122.45, 37.77, -122.35, 37.87]  # [min_lon, min_lat, max_lon, max_lat]
    bbox = BBox(bbox=bbox_coords, crs="EPSG:4326")
    bbox_size = bbox_to_dimensions(bbox, resolution=10)  # 10m per pixel

    # 3. Set a time range for the image
    time_interval = ("2023-08-01", "2023-08-02")  # Example date range

    # 4. Build the request to get a natural color (RGB) image
    request = SentinelHubRequest(
        data_folder="data",
        evalscript="""
            function setup() {
                return {
                    input: ["B04", "B03", "B02"],  // Red, Green, Blue bands
                    output: { bands: 3 }
                };
            }
            function evaluatePixel(sample) {
                return [sample.B04, sample.B03, sample.B02];
            }
        """,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=time_interval
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=bbox_size,
        config=config
    )

    # 5. Execute the request and save the image
    images = request.save_data()
    print("✅ Download complete! Saved to:", images)

if __name__ == "__main__":
    fetch_sentinel_image()
