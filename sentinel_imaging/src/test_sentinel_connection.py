import os
from dotenv import load_dotenv
from sentinelhub import SHConfig

# ✅ Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")  # Explicit path
load_dotenv(dotenv_path)

# ✅ Check if variables are actually loaded
print("Loaded CLIENT_ID:", os.getenv("SENTINELHUB_CLIENT_ID"))  # Debugging

# ✅ Set up Sentinel Hub config
config = SHConfig()
config.sh_client_id = os.getenv("SENTINELHUB_CLIENT_ID")
config.sh_client_secret = os.getenv("SENTINELHUB_CLIENT_SECRET")

# ✅ Debugging - Check if credentials loaded properly
if not config.sh_client_id or not config.sh_client_secret:
    print("❌ Missing Sentinel Hub credentials. Check your .env file.")
    exit(1)
else:
    print("✅ Sentinel Hub credentials loaded successfully!")

