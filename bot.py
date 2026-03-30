import asyncio
import logging
import os
import re
import tempfile
import time
from pathlib import Path

import yt_dlp
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

# ── CONFIG ─────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

semaphore = asyncio.Semaphore(3)

URL_PATTERN = re.compile(r"(https?://\S+)")

# ── EXTRACT TITLE FROM ANY LINK ────────────────────────
def extract_title(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("title")
        if title:
            text = title.text
            text = re.sub(r"[\|\-].*", "", text)  # clean extra text
            return text.strip()

    except:
        pass

    return "song"

# ── YT-DLP CONFIG ──────────────────────────────────────
def ydl_opts(out):
    return {
        "format": "bestaudio[ext=m4a]/bestaudio",
        "outtmpl": os.path.join(out, "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "writethumbnail": True,
    }

# ── FIND FILES ─────────────────────────────────────────
def find_files(folder):
    files = list(Path(folder).glob("*.*"))

    audio = None
    thumb = None

    for f in files:
        if f.suffix.lower() in [".m4a", ".mp3", ".webm", ".opus"]:
            audio = f
        elif f.suffix.lower() in [".jpg", ".webp"]:
            thumb = f

    return audio, thumb

# ── WAIT FILE RELEASE ──────────────────────────────────
def wait_file(path):
    for _ in range(10):
        try:
            with open(path, "rb"):
                return True
        except:
            time.sleep(0.5)
    return False

# ── DOWNLOAD ───────────────────────────────────────────
async def download(query, tmp):
    loop = asyncio.get_running_loop()

    def run(q):
        with yt_dlp.YoutubeDL(ydl_opts(tmp)) as ydl:
            return ydl.extract_info(f"ytsearch1:{q} official audio", download=True)

    info = await loop.run_in_executor(None, lambda: run(query))

    audio, thumb = find_files(tmp)

    if not audio:
        raise RuntimeError("Download failed")

    return str(audio), str(thumb) if thumb else None, info

# ── SEND POSTER ────────────────────────────────────────
async def send_poster(msg, thumb, title):
    if thumb:
        await msg.answer_photo(
            photo=FSInputFile(thumb),
            caption=f"🎵 {title}\n\n⏳ Preparing..."
        )

# ── SEND AUDIO ─────────────────────────────────────────
async def send_audio(msg, path, thumb, title):
    wait_file(path)

    await msg.answer_audio(
        audio=FSInputFile(path),
        caption=f"🎧 {title}",
        thumbnail=FSInputFile(thumb) if thumb else None
    )

# ── HANDLER ────────────────────────────────────────────
@dp.message(F.text)
async def handle(msg: Message):
    text = msg.text.strip()

    match = URL_PATTERN.search(text)
    if not match:
        await msg.answer("❌ Please send a music link")
        return

    url = match.group(0)

    status = await msg.answer("🔍 Processing link...")

    try:
        async with semaphore:
            with tempfile.TemporaryDirectory() as tmp:

                # 🔥 Extract title from ANY platform
                query = extract_title(url)

                # 🔥 Always search YouTube
                audio, thumb, info = await download(query, tmp)

                title = info.get("title", "Unknown")

                await send_poster(msg, thumb, title)

                await status.edit_text("⬇️ Downloading...")

                await send_audio(msg, audio, thumb, title)

                await status.delete()

    except Exception as e:
        logger.exception("ERROR:")
        await status.edit_text("❌ Failed to process this link")

# ── START ──────────────────────────────────────────────
@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer("Send any music link 🎵")

# ── MAIN ───────────────────────────────────────────────
async def main():
    print("Bot running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())