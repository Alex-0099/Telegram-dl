import sys
import asyncio
from tqdm import tqdm
from utils.parser import parse_chat_identifier, resolve_chat_entity
from utils.download import download_message_media, get_config

async def download_full(client, chat_input: str, override_types=None, limit=None):
    """
    Downloads all media from a specific Telegram chat, channel, group, or bot.
    """
    chat_input = chat_input.strip()
    
    # 1. Parse and clean chat identifier
    chat_identifier = parse_chat_identifier(chat_input)
    
    try:
        print(f"🔍 \033[1;36mResolving chat entity for '{chat_identifier}'...\033[0m")
        entity = await resolve_chat_entity(client, chat_input)
        
        # Determine human-readable chat name
        chat_title = getattr(entity, 'title', None) or getattr(entity, 'username', None) or str(entity.id)
        print(f"✅ \033[1;32mConnected to chat: {chat_title}\033[0m")
        
    except Exception as e:
        print(f"❌ \033[1;31m[ERROR] Could not resolve chat entity. Please check the name/ID/link and try again.\033[0m", file=sys.stderr)
        print(f"Details: {str(e)}", file=sys.stderr)
        return False
        
    print("📂 \033[1;36mScanning chat history for media... (This may take a moment for large chats)\033[0m")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    processed_count = 0
    
    # Get config and initialize worker pool
    config = get_config()
    max_concurrent = config.get("max_concurrent_downloads", 3)
    
    # Lock for thread-safe increments
    stats_lock = asyncio.Lock()
    
    # Worker queue to pass messages to download tasks
    queue = asyncio.Queue(maxsize=100)
    
    async def worker():
        nonlocal success_count, fail_count, skip_count
        while True:
            msg = await queue.get()
            if msg is None:
                queue.task_done()
                break
            
            try:
                success, result = await download_message_media(client, msg, entity.id, override_types)
                async with stats_lock:
                    if success:
                        if "File already exists" in result or "(Skipped)" in result:
                            skip_count += 1
                        else:
                            success_count += 1
                    else:
                        tqdm.write(f"❌ \033[1;31m[FAILED] Message ID {msg.id}: {result}\033[0m")
                        fail_count += 1
            except Exception as e:
                async with stats_lock:
                    tqdm.write(f"❌ \033[1;31m[ERROR] Error downloading message ID {msg.id}: {str(e)}\033[0m")
                    fail_count += 1
            finally:
                queue.task_done()

    # Start the download workers
    workers = [asyncio.create_task(worker()) for _ in range(max_concurrent)]
    
    try:
        # 2. Iterate through all messages in the chat history
        # If limit is specified, it will stop after parsing that number of messages
        async for message in client.iter_messages(entity, limit=limit):
            processed_count += 1
            
            # Print log every 100 messages scanned to show activity
            if processed_count % 100 == 0:
                tqdm.write(f"⚡ \033[1;30mScanned {processed_count} messages so far... (Downloaded: {success_count}, Skipped: {skip_count})\033[0m")
                
            if not message.media:
                async with stats_lock:
                    skip_count += 1
                continue
                
            # Queue the message for concurrent workers
            await queue.put(message)
                
    except Exception as e:
        tqdm.write(f"❌ \033[1;31m[ERROR] An error occurred during chat iteration: {str(e)}\033[0m")
    finally:
        # Send sentinels to workers to trigger exit
        for _ in range(max_concurrent):
            await queue.put(None)
            
        # Wait for all workers to complete
        await asyncio.gather(*workers)
        
    print(f"\n📊 \033[1;35mCHAT DOWNLOAD SUMMARY\033[0m")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💬 {'Chat Name:'.ljust(30)} \033[1;37m{chat_title}\033[0m")
    print(f"📝 {'Total messages scanned:'.ljust(30)} \033[1;37m{processed_count}\033[0m")
    print(f"📥 {'Successfully downloaded:'.ljust(30)} \033[1;32m{success_count}\033[0m")
    print(f"⏭️  {'Skipped (No media/existed):'.ljust(30)} \033[1;33m{skip_count}\033[0m")
    print(f"❌ {'Failed downloads:'.ljust(30)} \033[1;31m{fail_count}\033[0m")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    return True
