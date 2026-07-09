import sys
from utils.parser import parse_telegram_link, parse_chat_identifier
from utils.download import download_message_media

async def download_single(client, link_or_input: str, override_types=None):
    """
    Downloads media from a single Telegram message link.
    """
    link_or_input = link_or_input.strip()
    
    # 1. Parse link to extract chat identifier and message ID
    chat_id, message_id, _ = parse_telegram_link(link_or_input)
    
    if chat_id is None or message_id is None:
        print("❌ \033[1;31m[ERROR] Invalid message link format.\033[0m")
        print("💡 Please make sure the link is in the format: https://t.me/username/123 or https://t.me/c/12345/123")
        return False
        
    try:
        print(f"🔍 \033[1;36mFetching message {message_id} from chat {chat_id}...\033[0m")
        # 2. Get message object from Telegram
        message = await client.get_messages(chat_id, ids=message_id)
        
        if not message:
            print(f"❌ \033[1;31m[ERROR] Could not find message {message_id} in chat {chat_id}.\033[0m")
            return False
            
        if not message.media:
            print(f"⚠️ \033[1;33m[WARNING] Message {message_id} does not contain any downloadable media.\033[0m")
            return False
            
        # 3. Download the media
        success, result = await download_message_media(client, message, chat_id, override_types)
        if success:
            print(f"\n✅ \033[1;32m[SUCCESS] Media downloaded to: {result}\033[0m")
            return True
        else:
            print(f"\n❌ \033[1;31m[FAILED] Download failed: {result}\033[0m")
            return False
            
    except Exception as e:
        print(f"\n❌ \033[1;31m[ERROR] An error occurred while retrieving/downloading the message: {str(e)}\033[0m", file=sys.stderr)
        return False
