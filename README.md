# 🧙‍♂️ Magic Eden NFT Listings Telegram Bot (Cloud Run Edition)

Track newly listed NFTs on Magic Eden and get instant Telegram alerts – live from Google Cloud! 🚀

This bot supports **multiple collections**, runs fully on **Google Cloud Run**, and is **free to use** (within GCP Free Tier). No server required, no polling limits.

---

## 📦 Features

- 🔔 Telegram alerts for new NFT listings on Magic Eden  
- 🧑‍🎤 Supports multiple collections at once  
- ☁️ Fully serverless on Google Cloud Run  
- 🧠 Seen listings are remembered (per collection)  
- 🌐 Built-in Webserver for Cloud Run health checks  

---

## 🛠️ Prerequisites

1. A Telegram account & [@BotFather](https://t.me/BotFather) bot  
2. A Google Cloud account  
3. Basic familiarity with terminal & copy-paste  

---

## 🤖 Step-by-Step Setup

### 1️⃣ Create Your Telegram Bot

- Open [@BotFather](https://t.me/BotFather)
- Send `/newbot`
- Follow the instructions and save the **API Token**
- Get your `chat_id`:  
  - Write to your bot  
  - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`  
  - Copy your numeric chat ID  

---

### 2️⃣ Clone the Project

```bash
git clone https://github.com/YOUR_USERNAME/magiceden-telegram-bot.git
cd magiceden-telegram-bot
```

---

### 3️⃣ Create .env File
```
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_numeric_chat_id
COLLECTIONS=meatbags,meatbags_geocache
```
✅ You can monitor any Magic Eden collection by using its slug from the URL, e.g. https://magiceden.io/marketplace/meatbags

---

### 4️⃣ Setup Google Cloud Project
- Go to https://console.cloud.google.com

- Create a new project (e.g. magiceden-bot)

- Enable these APIs: `Cloud Run, Cloud Build, Artifact Registry`

--- 

### 5️⃣ Deploy to Cloud Run from Cloud Shell

Make sure your folder contains:
```bash
magiceden_bot.py
.env
requirements.txt
Dockerfile
.dockerignore
```
📄 requirements.txt
```nginx
requests
python-telegram-bot
python-dotenv
flask
```
🐳 Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "magiceden_bot.py"]
```
📁 .dockerignore
```bash
.env
__pycache__/
seen_*.json
```
⏫ Build & Deploy
```bash
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/magiceden-bot
```
Then deploy:
```bash
gcloud run deploy magiceden-bot \
  --image gcr.io/$(gcloud config get-value project)/magiceden-bot \
  --platform managed \
  --region europe-west1 \
  --memory 512Mi \
  --timeout=900 \
  --allow-unauthenticated \
  --env-vars-file .env
```
---
### 🚦 Keep It Alive
Google Cloud Run stops idle containers.

Use [UptimeRobot](https://uptimerobot.com/) to ping your bot every 5–10 minutes:
```arduino
https://your-cloud-run-url/
```
---
### ✅ Done!
You’re now monitoring Magic Eden collections in real time 🚀
---
### 🧪 Optional: Debug & Reset
🔁 Reset Seen Listings
```bash
rm seen_*.json
```
### 🧩 Force Telegram Test Message
Add this at the top of `monitor_listings()`:
```python
await bot.send_message(chat_id=CHAT_ID, text="🚀 Bot restarted & watching Magic Eden.")
```
---
### 🤝 Credits
Built by degen dev Wealthior. Inspired by real pain watching Magic Eden manually.
---
### 🔐 Security Tip
Never commit `.env` or real tokens to public GitHub.
Use `.gitignore`:
```bash
.env
seen_*.json
__pycache__/
```
---
Happy sniping ✌️