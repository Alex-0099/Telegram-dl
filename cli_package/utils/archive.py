import os
import sqlite3
from datetime import datetime

from utils.auth import PROJECT_ROOT

# Resolve the database path to the project root directory
DB_PATH = os.path.join(PROJECT_ROOT, 'archive.db')

def init_db():
    """Initializes the SQLite archive database and creates the downloads table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the archive table with metadata columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archive (
            chat_id TEXT,
            message_id INTEGER,
            filename TEXT,
            file_size INTEGER,
            downloaded_at TEXT,
            chat_name TEXT,
            caption TEXT,
            media_type TEXT,
            PRIMARY KEY (chat_id, message_id)
        )
    ''')
    
    # Dynamically alter table for older databases
    for col in [("chat_name", "TEXT"), ("caption", "TEXT"), ("media_type", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE archive ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            # Column already exists
            pass
            
    conn.commit()
    conn.close()

def is_archived(chat_id: str, message_id: int) -> bool:
    """Checks if a message media has already been downloaded and archived."""
    init_db()  # Ensure DB is initialized
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM archive WHERE chat_id = ? AND message_id = ?",
        (str(chat_id), message_id)
    )
    row = cursor.fetchone()
    
    conn.close()
    return row is not None

def add_to_archive(chat_id: str, message_id: int, filename: str, file_size: int, chat_name: str = "", caption: str = "", media_type: str = ""):
    """Adds a downloaded message media record with rich metadata to the archive database."""
    init_db()  # Ensure DB is initialized
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO archive (chat_id, message_id, filename, file_size, downloaded_at, chat_name, caption, media_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(chat_id), message_id, filename, file_size, now_str, chat_name, caption, media_type)
        )
        conn.commit()
    except Exception as e:
        print(f"\n⚠️ [DATABASE WARNING] Failed to archive download: {str(e)}")
    finally:
        conn.close()
