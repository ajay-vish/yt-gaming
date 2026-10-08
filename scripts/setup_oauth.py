#!/usr/bin/env python3
"""
YouTube OAuth 2.0 Credentials Setup Tool.
Run this locally once to authenticate your YouTube channel and obtain:
- YT_CLIENT_ID
- YT_CLIENT_SECRET
- YT_REFRESH_TOKEN
"""

import json
import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Error: google-auth-oauthlib is required.")
    print("Run: pip install google-auth-oauthlib")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.readonly"
]

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
CLIENT_SECRET_FILE = SCRIPTS_DIR / "client_secret.json"

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    print("=" * 70)
    print("YouTube OAuth 2.0 Setup for Channel Automation")
    print("=" * 70)
    
    if not CLIENT_SECRET_FILE.exists():
        print(f"\n[Action Required] client_secret.json not found at: {CLIENT_SECRET_FILE}")
        print("\nSteps to download it:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create or select a project.")
        print("3. Enable 'YouTube Data API v3' in APIs & Services -> Library.")
        print("4. Configure OAuth Consent Screen (External, add your Google account as test user).")
        print("5. Go to Credentials -> Create Credentials -> OAuth client ID -> Desktop App.")
        print("6. Download JSON and save it as 'scripts/client_secret.json'.")
        print("=" * 70)
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
    print("\nOpening your browser for Google authentication...")
    print("Please log in with the Google Account that manages your YouTube channel.")
    creds = flow.run_local_server(port=0)

    # Read client_id and client_secret from JSON
    with open(CLIENT_SECRET_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        installed = data.get("installed") or data.get("web") or {}
        client_id = installed.get("client_id", "")
        client_secret = installed.get("client_secret", "")

    print("\n" + "=" * 70)
    print("Authentication Successful! Copy these values:")
    print("=" * 70)
    print(f"YT_CLIENT_ID={client_id}")
    print(f"YT_CLIENT_SECRET={client_secret}")
    print(f"YT_REFRESH_TOKEN={creds.refresh_token}")
    print("=" * 70)
    print("\nAdd these to your .env file locally and to your GitHub Repo Secrets for Actions!")

if __name__ == "__main__":
    main()
