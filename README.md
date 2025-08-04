# I-House NYC Waitlist Telegram Bot

This bot logs into the I-House NYC waitlist portal every 5 minutes and sends you a Telegram message when a room might be available.

## 📦 Setup

1. Rename `.env.example` to `.env` and add your details.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python ihouse_checker.py
```

## 🚀 Deploy on Render

- Connect to GitHub
- Set build command: `pip install -r requirements.txt`
- Set start command: `python ihouse_checker.py`
- Add environment variables: `IHOUSE_USERNAME`, `IHOUSE_PASSWORD`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`

