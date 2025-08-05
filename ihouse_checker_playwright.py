import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import os
import time

# Get environment variables
USERNAME = os.getenv("IHOUSE_USERNAME")
PASSWORD = os.getenv("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/C80683C9/25/750/Waitlist-Initial_Selection?UrlToken=2002B365&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

room_found = False  # Global flag to avoid repeated spam


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❗ Telegram error:", e)


async def spam_alerts():
    messages = [
        "🚨 ROOM AVAILABLE! CHECK NOW!",
        "📢 WAKE UP BRO!",
        "✅ ROOM FOUND!",
        "💥 I-HOUSE ROOM IS OPEN!",
        "🔔 RUN TO THE PORTAL!"
    ]
    while room_found:
        for msg in messages:
            send_telegram(msg)
            await asyncio.sleep(2)


async def check_availability():
    global room_found
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
            await page.wait_for_url("**/Home-Welcome_to_the_I_Hou**", timeout=15000)

            # Go to waitlist page
            await page.goto(WAITLIST_URL)
            await page.wait_for_load_state("networkidle")
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            # Check room availability
            no_rooms_block = soup.find("div", class_="alert-nonefound alert")
            if no_rooms_block and "We couldn't find any available rooms" in no_rooms_block.text:
                print("❌ No rooms available.")
                room_found = False  # Reset
            else:
                if not room_found:
                    print("✅ Rooms might be available!")
                    room_found = True
                    asyncio.create_task(spam_alerts())

            await browser.close()

    except Exception as e:
        error_msg = f"❗ Bot error: {str(e)}"
        print(error_msg)
        send_telegram(error_msg)


async def heartbeat():
    while True:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        send_telegram(f"⏱️ Still checking for rooms... ({now})")
        await asyncio.sleep(1800)  # 10 minutes

async def main_loop():
    send_telegram("🤖 I-House room checker bot deployed and running!")
    print("🤖 Bot deployed and running using Playwright...")

    asyncio.create_task(heartbeat())  # Start heartbeat loop

    while True:
        await check_availability()
        await asyncio.sleep(180)  # wait 5 mins before next check


if __name__ == "__main__":
    asyncio.run(main_loop())
