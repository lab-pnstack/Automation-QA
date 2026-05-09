# utils/driver_setup.py
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

def get_driver():
    browser = os.getenv("BROWSER", BROWSER).lower()
    headless = os.getenv("HEADLESS", str(HEADLESS)).lower() == "true"

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Install driver and get the correct executable path
        driver_path = ChromeDriverManager().install()

        # Fix: webdriver-manager sometimes returns wrong file
        # The actual chromedriver is in the same directory
        if not os.path.isfile(driver_path) or not os.access(driver_path, os.X_OK):
            # Search for the actual chromedriver executable
            driver_dir = os.path.dirname(driver_path)

            # Look for chromedriver in the directory and subdirectories
            possible_paths = [
                os.path.join(driver_dir, 'chromedriver'),
                os.path.join(driver_dir, 'chromedriver-linux64', 'chromedriver'),
                os.path.join(driver_dir, 'chromedriver-mac-x64', 'chromedriver'),
                os.path.join(driver_dir, 'chromedriver-win64', 'chromedriver.exe'),
            ]

            # Also search recursively
            for pattern in ['**/chromedriver', '**/chromedriver.exe']:
                found = glob.glob(os.path.join(driver_dir, pattern), recursive=True)
                possible_paths.extend(found)

            # Find the first executable file
            for path in possible_paths:
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    driver_path = path
                    break

        driver = webdriver.Chrome(
            service=ChromeService(driver_path),
            options=options
        )

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    else:
        raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome' or 'firefox'.")

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver