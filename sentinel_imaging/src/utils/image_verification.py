from PIL import Image
from pathlib import Path

def verify_image(image_path: str = None) -> bool:
    """
    Verify a downloaded Sentinel image.
    
    Args:
        image_path: Optional path to specific image. If None, checks latest in data dir.
        
    Returns:
        bool: True if verification successful, False otherwise.
    """
    
    # Find image to verify
    if image_path is None:
        data_dir = Path("data")
        if not data_dir.exists():
            print("❌ Data directory not found")
            return False
            
        image_files = list(data_dir.glob("*.tiff"))
        if not image_files:
            print("❌ No images found in data directory")
            return False
            
        image_path = sorted(image_files)[-1]
    else:
        image_path = Path(image_path)
        if not image_path.exists():
            print(f"❌ Image not found: {image_path}")
            return False

    try:
        # Open and verify image
        with Image.open(image_path) as img:
            print(f"\n✅ Image verification successful:")
            print(f"  - Filename: {image_path.name}")
            print(f"  - Size: {img.size}")
            print(f"  - Mode: {img.mode}")
            print(f"  - Format: {img.format}")
            print(f"  - File size: {image_path.stat().st_size / (1024*1024):.2f} MB")
            return True
            
    except Exception as e:
        print(f"❌ Error verifying image: {str(e)}")
        return False

if __name__ == "__main__":
    verify_image()