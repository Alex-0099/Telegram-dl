import os
import sys
from dotenv import load_dotenv
from telethon import TelegramClient

# Resolve paths relative to project root
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = os.path.dirname(sys.executable)
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
SESSION_PATH = os.path.join(PROJECT_ROOT, 'telegram_dl_session')

# Load environment variables
load_dotenv(ENV_PATH)

import json

def get_client():
    """
    Initializes and returns the Telethon TelegramClient.
    If the client is not authenticated, it will prompt for login in the terminal.
    Allows fallback to config.json or interactive user input if credentials are missing.
    """
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')

    # Try reading from config.json
    config_path = os.path.join(PROJECT_ROOT, 'config.json')
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception:
            pass

    if not api_id:
        api_id = config.get('api_id')
    if not api_hash:
        api_hash = config.get('api_hash')
    if not phone:
        phone = config.get('phone')

    # Prompt user if credentials are not provided anywhere
    if not api_id or not api_hash:
        print("\n🔑 \033[1;36m[SETUP] Telegram API credentials not found.\033[0m")
        print("Please obtain your developer API ID and API Hash from: \033[1;34mhttps://my.telegram.org\033[0m")
        
        while not api_id:
            val = input("📞 Enter your API ID (integer): ").strip()
            if val.isdigit():
                api_id = int(val)
            else:
                print("❌ API ID must be a valid integer.")
                
        while not api_hash:
            val = input("🔑 Enter your API Hash: ").strip()
            if val:
                api_hash = val
            else:
                print("❌ API Hash cannot be empty.")
                
        if not phone:
            val = input("📞 Enter your Phone Number (optional, including country code, e.g. +1234567890): ").strip()
            if val:
                phone = val

        # Save to config.json for convenience
        config['api_id'] = api_id
        config['api_hash'] = api_hash
        if phone:
            config['phone'] = phone
            
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            print("✅ Credentials saved to config.json successfully.")
        except Exception as e:
            print(f"⚠️ Failed to save credentials to config.json: {str(e)}")

    try:
        api_id = int(api_id)
    except ValueError:
        print("❌ \033[1;31m[ERROR] TELEGRAM_API_ID must be a valid integer.\033[0m", file=sys.stderr)
        sys.exit(1)

    # Instantiate the client (session name/path SESSION_PATH)
    client = TelegramClient(SESSION_PATH, api_id, api_hash)
    return client, phone

async def authenticate_client(client, phone=None):
    """
    Authenticates the client using start().
    If a session does not exist, start() prompts the user on the console 
    for their phone number (if not provided), verification code, and 2FA password (if enabled).
    """
    print("📡 \033[1;36mConnecting to Telegram...\033[0m")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("🔑 \033[1;33mNot authorized. Initiating login process...\033[0m")
        if not phone:
            phone = input("📞 Enter your phone number (including country code, e.g., +1234567890): ")
        
        # client.start will handle the verification code input and 2FA password prompting
        await client.start(phone=lambda: phone)
        
    print("✅ \033[1;32mAuthentication successful!\033[0m")
    return client
