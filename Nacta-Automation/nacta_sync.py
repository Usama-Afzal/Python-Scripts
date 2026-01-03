#!/usr/bin/env python3
import os
import time
import shutil
import smtplib
import requests
import psutil
import subprocess
import traceback
from datetime import datetime
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from dotenv import load_dotenv

# Load all configurations from .env
load_dotenv()

# --- Configuration (Sanitized and Loaded from .env) ---
BASE_DIR = os.getenv("BASE_DIR", "/etc/scripts/nacta")
DIRS = {
    "DOWNLOAD": os.path.join(BASE_DIR, "data/downloads"),
    "BACKUP": os.path.join(BASE_DIR, "data/backup"),
    "LOGS": os.path.join(BASE_DIR, "logs"),
    "DEBUG": os.path.join(BASE_DIR, "logs/debug"),
}
LOG_FILE = os.path.join(DIRS["LOGS"], f"nacta_{datetime.now().strftime('%Y-%m-%d')}.log")

CHROME_BIN = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
CHROMEDRIVER_BIN = os.getenv("CHROMEDRIVER_BIN", "/usr/bin/chromedriver")

# Remote Server Settings
REMOTE = {
    "HOST": os.getenv("REMOTE_HOST"),
    "USER": os.getenv("REMOTE_USER"),
    "PORT": os.getenv("REMOTE_PORT", "22"),
    "KEY": os.getenv("REMOTE_KEY_PATH"),
    "PATHS": {
        "ProscribedPersons": os.getenv("REMOTE_PATH_NOTIFY"),
        "DenotifiedProscribedPersons": os.getenv("REMOTE_PATH_DENOTIFY")
    }
}

# Notification Settings
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#nacta-alerts")
EMAIL_CONF = {
    "SERVER": os.getenv("SMTP_SERVER"),
    "PORT": int(os.getenv("SMTP_PORT", 25)),
    "FROM": os.getenv("EMAIL_FROM"),
    "TO": os.getenv("EMAIL_TO_LIST", "").split(",")
}

URLS = {
    'https://nfs.nacta.gov.pk/': 'ProscribedPersons',
    'https://nfs.nacta.gov.pk/denotified': 'DenotifiedProscribedPersons'
}

# --- Utility Functions (Restored from your original code) ---

def log(msg, level="INFO"):
    entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {msg}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def clean_chrome():
    [cite_start]"""Restored: Kill all Chrome and ChromeDriver processes [cite: 4]"""
    killed = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = (proc.info['name'] or '').lower()
            if 'chrome' in name or 'chromedriver' in name:
                proc.kill()
                killed.append(f"{proc.info['name']}({proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if killed:
        log(f"Killed processes: {', '.join(killed)}")

def create_driver():
    [cite_start]"""Restored: Optimal headless configuration [cite: 8, 10, 11]"""
    opts = webdriver.ChromeOptions()
    opts.binary_location = CHROME_BIN
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    prefs = {"download.default_directory": DIRS["DOWNLOAD"]}
    opts.add_experimental_option("prefs", prefs)
    
    service = Service(CHROMEDRIVER_BIN)
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(120)
    return driver

def find_download_button(driver):
    [cite_start]"""Restored: Advanced XPath strategy list [cite: 16, 17, 18]"""
    strategies = [
        ("//button[contains(., 'JSON')]", "Button with JSON"),
        ("//a[contains(., 'JSON')]", "Anchor with JSON"),
        ("//a[contains(text(), 'Download')]", "Anchor with Download text")
    ]
    for xpath, desc in strategies:
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if element.is_displayed():
                log(f"Found button: {desc}")
                return element
        except:
            continue
    return None

def send_notification(subject, body_lines, success=True):
    [cite_start]"""Restored: Dual Email & Slack reporting [cite: 32, 33, 34, 35]"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS ✓" if success else "FAILURE ✗"
    msg_content = f"Status: {status}\nTimestamp: {timestamp}\n\n" + "\n".join(body_lines)

    # Email Logic
    if EMAIL_CONF["SERVER"]:
        try:
            msg = MIMEText(msg_content)
            msg['Subject'] = f"[{'OK' if success else 'ALERT'}] {subject}"
            msg['From'] = EMAIL_CONF['FROM']
            msg['To'] = ", ".join(EMAIL_CONF['TO'])
            with smtplib.SMTP(EMAIL_CONF['SERVER'], EMAIL_CONF['PORT']) as server:
                server.send_message(msg)
        except Exception as e:
            log(f"Email failed: {e}", "ERROR")

    # Slack Logic
    if SLACK_URL:
        try:
            payload = {"text": f"*{subject}*\n```{msg_content}```"}
            requests.post(SLACK_URL, json=payload, timeout=10)
        except Exception as e:
            log(f"Slack failed: {e}", "ERROR")

def rsync_file(local_path, file_prefix):
    [cite_start]"""Restored: Precise rsync command with SSH key support [cite: 37]"""
    remote_path = REMOTE["PATHS"].get(file_prefix)
    cmd = [
        "rsync", "-avz",
        "-e", f"ssh -i {REMOTE['KEY']} -p {REMOTE['PORT']} -o StrictHostKeyChecking=no",
        local_path,
        f"{REMOTE['USER']}@{REMOTE['HOST']}:{remote_path}/"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        log(f"Rsync error: {e}", "ERROR")
        return False

def process_url(url, prefix):
    driver = create_driver()
    try:
        driver.get(url)
        button = find_download_button(driver)
        if not button:
            raise Exception("Download button not found")
        
        button.click()
        time.sleep(15) # Wait for download
        
        # [cite_start]File management logic [cite: 51, 52]
        files = os.listdir(DIRS["DOWNLOAD"])
        if not files:
            raise Exception("No file downloaded")
        
        fname = files[0]
        src = os.path.join(DIRS["DOWNLOAD"], fname)
        new_name = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        dest = os.path.join(DIRS["DOWNLOAD"], new_name)
        os.rename(src, dest)
        
        if rsync_file(dest, prefix):
            os.remove(dest)
            return new_name
    finally:
        driver.quit()

def main():
    log("NACTA Download Script Started (PRODUCTION)")
    for path in DIRS.values():
        os.makedirs(path, exist_ok=True)

    clean_chrome()
    processed = []
    errors = []

    for url, prefix in URLS.items():
        try:
            filename = process_url(url, prefix)
            processed.append(filename)
        except Exception as e:
            errors.append(f"{prefix}: {str(e)}")

    # [cite_start]Final Reporting [cite: 67, 68]
    if errors:
        send_notification("NACTA Sync Partial Failure", errors, success=False)
    else:
        send_notification("NACTA Sync Successful", processed, success=True)

if __name__ == "__main__":
    main()
