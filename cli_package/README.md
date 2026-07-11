# Telegram Downloader CLI Package 📦

This directory contains the source code and packaging assets to compile and run the standalone Windows CLI executable for **Telegram Downloader (V3.8.5)**.

---

## 🚀 How to Run the Executable

You can find the pre-compiled executable in the `dist/` directory:
👉 **[telegram-dl.exe](dist/telegram-dl.exe)**

### Features:
* **Zero Setup**: If no `.env` file exists in the directory, the application will launch and prompt you interactively to enter your `API ID` and `API Hash` (which you can get for free from [my.telegram.org](https://my.telegram.org)).
* **Auto-Save**: The entered credentials will be automatically saved to `config.json` so you only have to enter them once.
* **Portable**: You can move this single `.exe` file anywhere on your computer or run it from a USB stick.

---

## 🛠️ How to Compile It Yourself

If you modify the source files under `modules/` or `utils/` and want to compile a new `.exe` file:

1. **Install Dependencies**:
   Open a terminal in this directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Compiler Script**:
   Execute the automated build script:
   ```bash
   python build.py
   ```
   * The script will automatically install PyInstaller if it is missing, compile the application into a single standalone file, and clean up all temporary build directory clutter afterward.
   * The fresh executable will be placed in the `dist/` directory.
