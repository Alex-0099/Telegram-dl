# Telegram Downloader V2.0.0 (CLI) 🚀

An advanced, high-performance, asynchronous userbot-style Telegram media downloader built in Python using the **Telethon** MTProto library. 

This downloader provides a sleek, modern keyboard-navigable terminal interface (TUI) to retrieve photos, videos, documents, audios, voice notes, and stickers from public and private groups, channels, chats, and bots.

---

## 🌟 V2.0.0 Key Features

* **Bypasses Save Restrictions**: Naturally bypasses Telegram's client-side copy/forwarding restrictions (e.g., *"Restrict saving content"* in private groups/channels) by directly requesting raw MTProto file chunks.
* **Resumable Chunk Downloads**: Tracks `.part` temporary downloads on disk. If interrupted, it automatically truncates and resumes from the nearest **4KB boundary** (Telegram requirement). Uses maximum **512KB chunk sizes** to minimize network request latency, boosting download speeds by up to 4x.
* **Live Monitor Daemon**: Automatically watches specified chats in the background. Features **Bot Session Grouping** with custom inactivity gaps, grouping files sent by request bots into separate time-clustered subfolders (e.g. `Session_2026-07-09_12-30-00/`).
* **Sleek Web Gallery Generator**: Automatically compiles downloaded files into responsive, glassmorphic HTML galleries (`gallery.html`) containing search filtering, topic/chat views, audio players, video players, and image lightbox overlays.
* **Advanced Media Utilities**:
  * **Audio Extractor**: Converts videos to high-quality MP3s via `ffmpeg` (optionally automated post-download).
  * **Sticker Converter**: Renders WebP stickers to PNG, and decompresses `.tgs` animated stickers to Lottie JSON.
  * **Batch Rename**: Clean names, prefix indexation, and random alphanumeric masks.
  * **Folder Organizer**: Sorts downloaded folders into categorized directories (Images, Videos, Docs, Audio, Archives).
  * **7-Zip password archiving**: Creates secure, AES-256 encrypted `.7z` or `.zip` archives.
* **Cloud Sync & Telegram Mirroring**:
  * **Rclone Integration**: Asynchronously moves/copies downloaded files to Google Drive, Mega, OneDrive, etc., in the background (with optional local cleanup).
  * **Telegram Mirror**: Re-uploads downloaded files in real-time to another private channel or group.
* **Offline Search & History**: Queries your download history by keywords, chats, or media types. Integrates with the system file explorer to highlight files directly in **Windows Explorer**, **macOS Finder**, or **Linux File Manager**.
* **Global Bandwidth Throttling**: Configure a maximum download speed limit (using Token Bucket rate limiting) across all active concurrent threads.

---

## 📁 File Structure

```text
telegram-dl/
├── .env                  # API Credentials (created by copying .env.example)
├── .env.example          # Template for credentials
├── .gitignore            # Git exclusion rules
├── config.json           # Interactive configuration parameters (auto-generated)
├── requirements.txt      # Python libraries list
├── telegram-dl.py        # Main TUI & Menu loop driver
├── telegram-dl.bat        # Global launch batch script for Windows PATH
├── modules/
│   ├── single.py         # Single file downloader module
│   ├── range.py          # Message range downloader module (with server-side topic filter)
│   ├── full.py           # Full chat history downloader module
│   ├── daemon.py         # Live Monitor Daemon (with bot session clustering)
│   ├── search.py         # Offline search TUI panel
│   ├── cloud.py          # Rclone upload and mirroring setup panel
│   └── utilities.py      # Media extraction, renaming, and compression panel
└── utils/
    ├── archive.py        # SQLite3 download history database manager
    ├── auth.py           # MTProto authentication handler
    ├── parser.py         # Telegram link & ID parsing utilities
    ├── gallery_template.py # Separation of HTML/CSS/JS gallery code
    └── download.py       # Core downloader, semaphores, and path resolver
```

---

## ⚙️ Prerequisites & Setup

### 1. Retrieve Telegram API Credentials
1. Log in to [my.telegram.org](https://my.telegram.org) using your Telegram phone number.
2. Go to **API development tools**.
3. Create a new application (e.g. Title: `Media Downloader CLI`, Short name: `mymediadl`, Platform: `Desktop`).
4. Note down your `api_id` and `api_hash`.

### 2. Configure Environment Secrets
Duplicate the `.env.example` file, rename it to `.env`, and fill in your credentials:
```ini
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number_with_country_code # e.g. +1234567890
```

### 3. Install Dependencies
Make sure you have python 3.8+ installed. Run:
```bash
pip install -r requirements.txt
```
> [!NOTE]
> System dependencies: `ffmpeg` is required for audio extraction, `7-Zip` (`7z`) is required for password-protected archiving, and `rclone` is required for cloud upload backups.

---

## 🚀 Running the Downloader

Run the main script to launch the interactive TUI:
```bash
python telegram-dl.py
```

### Run Globally from Anywhere (Windows)
We have provided a batch file `telegram-dl.bat`. If you add the `C:\Users\LENOVO\telegram-dl` directory to your User or System `PATH` environment variable, you can run:
```cmd
telegram-dl
```
from any folder on your computer!

---

## ⚠️ Notes & Security Best Practices

* **Rate Limits**: If you run a **Full Download** on large channels with thousands of items, Telegram may trigger a `FloodWait`. The script will automatically sleep and resume, but it is best to respect rate limits or cap the download speed in the Config menu.
* **Security Warnings**: 
  > [!CAUTION]
  > **DO NOT** commit or upload the following files to GitHub or any public repository:
  > * `.env` (Contains your secret Telegram API keys)
  > * `*.session` and `*.session-journal` (Contains active login session tokens)
  > * `config.json` (Contains your list of monitored chats and Rclone remote configurations)
  > * `archive.db` (Contains your private download history)
  >
  > These are already added to `.gitignore` by default. Do not force-commit them.
