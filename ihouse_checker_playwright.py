
import os
import time
import requests
from playwright.sync_api import sync_playwright

# Load credentials from environment
USERNAME = os.environ.get("IHOUSE_USERNAME")
PASSWORD = os.environ.get("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login?returnUrl=%2FStarRezPortalX%2F470CAB25%2F1%2F1%2FHome-Welcome_to_the_I_Hou%3FUrlToken%3D5392BC13"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/3FB6D5B6/25/750/Waitlist-Initial_Selection?UrlToken=5392BC13&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

def login_and_check():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(LOGIN_URL)
        page.fill("input#username", USERNAME)
        page.fill("input#password", PASSWORD)
        page.click("button#loginbtn")
        page.wait_for_timeout(5000)

        page.goto(WAITLIST_URL)
        page.wait_for_timeout(5000)

        if "We couldn't find any available rooms" not in page.content():
            send_telegram("🚨 Possible room availability detected! Check the I-House portal.")
        else:
            print("❌ No rooms available.")

        browser.close()

send_telegram("✅ Bot deployed and running using Playwright.")

while True:
    try:
        login_and_check()
    except Exception as e:
        send_telegram(f"❗ Bot error: {e}")
    time.sleep(300)  # Wait 5 minutes before next check
