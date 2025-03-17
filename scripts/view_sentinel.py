import matplotlib.pyplot as plt
from pathlib import Path
import rasterio
import numpy as np

def enhance_image(image, percentile=(2, 98)):
    """Enhance image contrast using percentile normalization."""
    p_low, p_high = np.percentile(image, percentile)
    return np.clip((image - p_low) / (p_high - p_low), 0, 1)

def view_sentinel_image():
    """View the latest downloaded Sentinel image."""
    data_dir = Path("data")
    image_files = list(data_dir.glob("*.tiff"))
    
    if not image_files:
        print("❌ No images found in data directory")
        return
        
    latest_image = sorted(image_files)[-1]
    print(f"📄 Loading image: {latest_image}")
    
    try:
        with rasterio.open(latest_image) as src:
            # Read and enhance image
            image = src.read()
            enhanced = np.dstack([enhance_image(band) for band in image])
            
            # Create figure
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            # Original image
            ax1.imshow(np.transpose(image, (1, 2, 0)) / 255)
            ax1.set_title("Original Image")
            
            # Enhanced image
            ax2.imshow(enhanced)
            ax2.set_title("Enhanced Image")
            
            # Add metadata
            plt.figtext(0.02, 0.02, 
                       f"Image Size: {image.shape}\n"
                       f"Location: San Francisco Bay Area\n"
                       f"Date: {latest_image.stem.split('_')[-1]}",
                       fontsize=8)
            
            plt.tight_layout()
            plt.show()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    view_sentinel_image()