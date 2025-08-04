import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import os
import time
import schedule

# Get environment variables
USERNAME = os.getenv("IHOUSE_USERNAME")
PASSWORD = os.getenv("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/C80683C9/25/750/Waitlist-Initial_Selection?UrlToken=2002B365&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❗ Telegram error:", e)

async def check_availability():
    print("🔍 Checking room availability...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Login
            await page.goto(LOGIN_URL)
            await page.fill('input[name="Username"]', USERNAME)
            await page.fill('input[name="Password"]', PASSWORD)
            await page.click('button:has-text("Login")')

            # Wait for redirect
            await page.wait_for_url("**/Home-Welcome_to_the_I_Hou**", timeout=15000)

            # Navigate to waitlist page
            await page.goto(WAITLIST_URL)
            await page.wait_for_load_state("networkidle")

            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            # Look for "no rooms" message
            no_rooms_block = soup.find("div", class_="alert-nonefound alert")
            if no_rooms_block and "We couldn't find any available rooms" in no_rooms_block.text:
                print("❌ No rooms available.")
                send_telegram("❌ No rooms available.")
            else:
                print("✅ Rooms might be available!")
                send_telegram("✅ Rooms might be available! Go check now!")

            await browser.close()

    except Exception as e:
        error_msg = f"❗ Bot error: {str(e)}"
        print(error_msg)
        send_telegram(error_msg)

def run_bot():
    asyncio.run(check_availability())

if __name__ == "__main__":
    print("🤖 Bot deployed and running using Playwright...")
    send_telegram("🤖 I-House room checker bot deployed and running!")

    # Check once immediately, then every 5 mins
    run_bot()
    schedule.every(5).minutes.do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)
