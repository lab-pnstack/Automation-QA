# utils/helpers.py
import os, time
from datetime import datetime
from utils.config import SCREENSHOT_DIR

def take_screenshot(driver, name="screenshot"):
    """Chụp màn hình khi test fail."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{SCREENSHOT_DIR}{name}_{timestamp}.png"
    driver.save_screenshot(path)
    print(f"[Screenshot saved] {path}")
    return path

def wait_seconds(n=1):
    time.sleep(n)

def generate_email():
    """Tạo email ngẫu nhiên để test register."""
    from faker import Faker
    fake = Faker()
    return fake.email()