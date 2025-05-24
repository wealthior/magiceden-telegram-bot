import requests
import json
import asyncio
import os
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
COLLECTIONS = os.getenv("COLLECTIONS").split(",")
LIMIT = 100
SEEN_FILE = "seen_collections.json"
CHECK_INTERVAL = 60  # seconds

bot = Bot(token=BOT_TOKEN)
app = Flask('')
@app.route('/')

def home():
    return "✅ Multi-Collection MagiEden Bot runs."

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# 📁 File-Name per collection
def get_seen_file(collection):
    return f"seen_{collection}.json"

# 📥 Seen-Logik per collection
def load_seen(collection):
    try:
        with open(get_seen_file(collection), "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(collection, seen_set):
    with open(get_seen_file(collection), "w") as f:
        json.dump(list(seen_set), f)

# 🛰️ Listings request
def fetch_listings(collection):
    url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection}/listings?offset=0&limit={LIMIT}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

# 📲 Telegram notify
async def send_listing(nft, collection):
    name = nft["token"]["name"]
    price = nft["price"]
    mint = nft["token"]["mintAddress"]
    img = nft["token"]["image"]
    url = f"https://magiceden.io/item-details/{mint}"
    caption = f"🆕 [{collection}] {name}\n💰 {price} SOL\n🔗 {url}"
    await bot.send_photo(chat_id=CHAT_ID, photo=img, caption=caption)

# 🔁 Main Loop
async def monitor_listings():
    seen_map = {c: load_seen(c) for c in COLLECTIONS}

    while True:
        for collection in COLLECTIONS:
            try:
                listings = fetch_listings(collection)
                current_seen = set()
                for nft in listings:
                    mint = nft["token"]["mintAddress"]
                    current_seen.add(mint)
                    if mint not in seen_map[collection]:
                        await send_listing(nft, collection)
                seen_map[collection] = current_seen
                save_seen(collection, current_seen)
            except Exception as e:
                print(f"[Fehler in {collection}] {e}")
        await asyncio.sleep(CHECK_INTERVAL)

# ▶️ Start
if __name__ == "__main__":
    keep_alive() 
    asyncio.run(monitor_listings())