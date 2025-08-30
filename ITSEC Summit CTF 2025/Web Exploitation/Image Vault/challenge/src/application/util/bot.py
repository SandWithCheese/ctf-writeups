import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

active_visits = set()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def visit_url(target_url, ip):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--safebrowsing-disable-auto-update")
    chrome_options.add_argument("--media-cache-size=1")
    chrome_options.add_argument("--disk-cache-size=1")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://localhost:1337/login")
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(ADMIN_USERNAME)
        driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
        driver.execute_script("document.getElementById('loginBtn').click()")
        time.sleep(2)

        driver.get(target_url)
        time.sleep(15)

        print(f"[Visit Details] IP: {ip} visited URL: {target_url}")

    except Exception as e:
        print(f"[Visit Details] IP: {ip}, URL: {target_url}, Error: {e}")

    finally:
        driver.quit()
        active_visits.discard(ip)


