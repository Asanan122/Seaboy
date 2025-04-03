from sentinelhub import SHConfig
import os
from dotenv import load_dotenv
import requests

def get_sentinel_config():
    """Create and return a Sentinel Hub configuration for CDSE."""
    load_dotenv()
    
    config = SHConfig()
    
    # Set CDSE credentials
    config.sh_client_id = os.getenv('SENTINELHUB_CLIENT_ID')
    config.sh_client_secret = os.getenv('SENTINELHUB_CLIENT_SECRET')
    
    # Set CDSE endpoints
    config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
    config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
    config.services_url = 'https://sh.dataspace.copernicus.eu/api/v1'
    config.processing_api_url = 'https://sh.dataspace.copernicus.eu/api/v1/process'
    
    # Set CDSE instance
    config.instance_id = 'cdse'
    
    # Get and set access token
    try:
        response = requests.post(
            config.sh_token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': config.sh_client_id,
                'client_secret': config.sh_client_secret
            }
        )
        response.raise_for_status()
        token = response.json()['access_token']
        config.oauth_token = token
        
    except Exception as e:
        raise Exception(f"Failed to initialize CDSE configuration: {str(e)}")
    
    return config

sentinel_config = get_sentinel_config()