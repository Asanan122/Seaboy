import os
from dotenv import load_dotenv
from sentinelhub import SHConfig

def get_sentinelhub_config():
    # Load environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")  # Explicit path
    load_dotenv(dotenv_path)

    config = SHConfig()
    config.sh_client_id = os.getenv("SENTINELHUB_CLIENT_ID")
    config.sh_client_secret = os.getenv("SENTINELHUB_CLIENT_SECRET")

    if not config.sh_client_id or not config.sh_client_secret:
        raise ValueError("❌ Missing Sentinel Hub credentials. Check your .env file.")

    return config

