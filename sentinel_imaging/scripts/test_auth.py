import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print values to debug
print("🔍 DEBUG - CLIENT_ID:", os.getenv("SENTINELHUB_CLIENT_ID"))
print("🔍 DEBUG - CLIENT_SECRET:", os.getenv("SENTINELHUB_CLIENT_SECRET")[:5] + "...(hidden)")
print("🔍 DEBUG - AUTH_URL:", os.getenv("SENTINELHUB_AUTH_URL"))

# Assign variables
CLIENT_ID = os.getenv("SENTINELHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("SENTINELHUB_CLIENT_SECRET")
AUTH_URL = os.getenv("SENTINELHUB_AUTH_URL")

# Ensure values exist
if not AUTH_URL or not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ ERROR: Missing required environment variables!")

# Request token
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(AUTH_URL, data=data)

if response.status_code == 200:
    print("✅ Successfully authenticated!")
    print("🔑 Access Token:", response.json().get("access_token")[:50] + "...")
else:
    print("❌ Authentication failed:", response.json())
