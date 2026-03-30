# 🎵 Telegram Music Downloader Bot

A powerful Telegram bot that downloads high-quality audio from **any music platform link** (Spotify, YouTube, SoundCloud, Apple Music, etc.) and sends it directly in chat with a clean UI.

---

## 🚀 Features

- 🎵 Supports multiple platforms:
  - Spotify  
  - YouTube / YouTube Music  
  - SoundCloud  
  - Apple Music  
  - Other music links  

- 🔄 Smart conversion:
  - Extracts song title from link  
  - Searches on YouTube  
  - Downloads best audio  

- 🖼 Rich UI:
  - Shows song poster (thumbnail)  
  - Displays download status  
  - Sends audio with thumbnail  

- ⚡ Performance:
  - Fast downloads (m4a format)  
  - Optimized for stability  
  - Handles errors gracefully  

---

## 🛠 Tech Stack

- Python 3.10+
- aiogram
- yt-dlp
- requests
- BeautifulSoup

---

## 📁 Project Structure
music-bot/
│
├── bot.py
├── requirements.txt
├── Procfile
├── .env


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
git clone https://github.com/Rajat-Solankii/Telegram-music-bot.git

cd music-bot

---

### 2️⃣ Install dependencies
pip install -r requirements.txt
---

### 3️⃣ Create `.env` file
BOT_TOKEN=your_telegram_bot_token
---

### 4️⃣ Run the bot
python bot.py
