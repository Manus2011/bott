import asyncio
from playwright.async_api import async_playwright
import telegram
import os

# Telegram Bot setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# I-House credentials from environment variables
USERNAME = os.getenv("IHO_USERNAME")
PASSWORD = os.getenv("IHO_PASSWORD")

# Correct waitlist page after login
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/C80683C9/25/750/Waitlist-Initial_Selection?UrlToken=2002B365&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

async def send_telegram_message(message: str):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def check_availability():
    try:
        await send_telegram_message("🤖 Bot deployed and running using Playwright!")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://ihnyc.starrezhousing.com/StarRezPortalX/Login")

            await page.wait_for_selector('input[name="Username"]', timeout=60000)
            await page.fill('input[name="Username"]', USERNAME)
            await page.fill('input[name="Password"]', PASSWORD)
            await page.click('button:has-text("Login")')

            await page.wait_for_load_state("networkidle")
            await page.goto(WAITLIST_URL)
            await page.wait_for_load_state("networkidle")

            content = await page.content()

            # Simple keyword check — adjust as needed
            if "No rooms available" in content or "currently full" in content:
                print("No availability.")
            else:
                await send_telegram_message("🚨 Room might be available! Go check now: " + WAITLIST_URL)

            await browser.close()

    except Exception as e:
        await send_telegram_message(f"❗ Bot error: {e}")

if __name__ == "__main__":
    asyncio.run(check_availability())
