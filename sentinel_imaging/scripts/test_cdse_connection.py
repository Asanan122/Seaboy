import requests
from src.config_sentinel import sentinel_config

def test_cdse_connection():
    """Test CDSE connection and endpoints."""
    config = sentinel_config
    
    # Print configuration
    print("🔍 Testing CDSE Configuration:")
    print(f"  Base URL: {config.base_url}")
    print(f"  Process URL: {config.processing_api_url}")
    print(f"  Token: {config.oauth_token[:30]}...")
    
    # Test endpoint
    try:
        headers = {
            'Authorization': f'Bearer {config.oauth_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            f"{config.base_url}/configuration/v1/wms/instances",
            headers=headers
        )
        response.raise_for_status()
        print("✅ Successfully connected to CDSE!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_cdse_connection()