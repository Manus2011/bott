import os
import time
import requests
import asyncio
from playwright.async_api import async_playwright

# Load credentials from environment
USERNAME = os.environ.get("IHOUSE_USERNAME")
PASSWORD = os.environ.get("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login?returnUrl=%2FStarRezPortalX%2F470CAB25%2F1%2F1%2FHome-Welcome_to_the_I_Hou%3FUrlToken%3D5392BC13"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/3FB6D5B6/25/750/Waitlist-Initial_Selection?UrlToken=5392BC13&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

def send_telegram(msg):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        print("Telegram alert failed.")

async def login_and_check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(LOGIN_URL, timeout=60000)
            await page.wait_for_selector("input#username", timeout=60000)
            await page.screenshot(path="login_page.png")

            await page.fill("input#username", USERNAME)
            await page.fill("input#password", PASSWORD)
            await page.click("button#loginbtn")
            await page.wait_for_timeout(5000)

            await page.goto(WAITLIST_URL, timeout=60000)
            await page.wait_for_timeout(5000)
            await page.screenshot(path="waitlist_page.png")

            content = await page.content()
            await browser.close()

            if "We couldn't find any available rooms" not in content:
                send_telegram("🚨 Possible room availability detected! Check the I-House portal.")
            else:
                print("❌ No rooms available.")

        except Exception as e:
            await page.screenshot(path="error_page.png")
            send_telegram(f"❗ Bot error: {e}")
            await browser.close()

# 🔁 Main loop
if __name__ == "__main__":
    send_telegram("✅ Bot deployed and running using Playwright.")
    while True:
        try:
            asyncio.run(login_and_check())
        except Exception as e:
            send_telegram(f"❗ Top-level bot error: {e}")
        time.sleep(300)  # Check every 5 mins
