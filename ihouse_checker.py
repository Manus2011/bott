import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load credentials from environment
USERNAME = os.environ.get("IHOUSE_USERNAME")
PASSWORD = os.environ.get("IHOUSE_PASSWORD")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/Login?returnUrl=%2FStarRezPortalX%2F470CAB25%2F1%2F1%2FHome-Welcome_to_the_I_Hou%3FUrlToken%3D5392BC13"
WAITLIST_URL = "https://ihnyc.starrezhousing.com/StarRezPortalX/3FB6D5B6/25/750/Waitlist-Initial_Selection?UrlToken=5392BC13&TermID=103&DateStart=Monday%2C%20September%201%2C%202025&DateEnd=Thursday%2C%20January%201%2C%202026"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

def login_and_check():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    time.sleep(3)
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    time.sleep(5)
    driver.get(WAITLIST_URL)
    time.sleep(5)
    page_text = driver.page_source
    driver.quit()

    if "We couldn't find any available rooms" not in page_text:
        send_telegram("🚨 Possible room availability detected! Check the I-House portal.")
    else:
        print("❌ No rooms available.")

while True:
    try:
        login_and_check()
    except Exception as e:
        send_telegram(f"❗ Bot error: {e}")
    time.sleep(300)  # 5 minutes
