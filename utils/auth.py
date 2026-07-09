import os
import sys
from dotenv import load_dotenv
from telethon import TelegramClient

# Resolve paths relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
SESSION_PATH = os.path.join(PROJECT_ROOT, 'telegram_dl_session')

# Load environment variables
load_dotenv(ENV_PATH)

def get_client():
    """
    Initializes and returns the Telethon TelegramClient.
    If the client is not authenticated, it will prompt for login in the terminal.
    """
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')

    if not api_id or not api_hash:
        print("❌ \033[1;31m[ERROR] TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in the .env file.\033[0m", file=sys.stderr)
        print("💡 Please check your .env file or copy from .env.example", file=sys.stderr)
        sys.exit(1)

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
