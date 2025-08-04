import os
import asyncio
from playwright.async_api import async_playwright
import requests

# Load credentials from environment variables
USERNAME = os.environ.get("IHOUSE_USERNAME")
PASSWORD = os.environ.get("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login?returnUrl=%2FStarRezPortalX%2FA6E9F565%2F1%2F1%2FHome-Welcome_to_the_I_Hou%3FUrlToken%3DD2E7C655"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/3FB6D5B6/25/750/Waitlist-Initial_Selection?UrlToken=5392BC13&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

async def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

async def login_and_check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(LOGIN_URL, timeout=60000)
        await page.fill('input[name="Username"]', USERNAME)
        await page.fill('input[name="Password"]', PASSWORD)
        await page.click('button:has-text("Login")')
        await page.wait_for_url("**/Home-*", timeout=15000)

        await page.goto(WAITLIST_URL)
        content = await page.content()
        await browser.close()

        if "We couldn't find any available rooms" not in content:
            await send_telegram("🚨 Possible room availability detected! Check the I-House portal.")
        else:
            print("❌ No rooms available.")

async def main():
    await send_telegram("🤖 Bot deployed and running using Playwright.")
    while True:
        try:
            await login_and_check()
        except Exception as e:
            await send_telegram(f"❗ Bot error: {e}")
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
