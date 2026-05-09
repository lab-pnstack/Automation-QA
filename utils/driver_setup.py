# utils/driver_setup.py
import os
import glob
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)

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

        # Install driver and get the path
        driver_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriverManager returned: {driver_path}")

        # Fix: webdriver-manager sometimes returns wrong file (THIRD_PARTY_NOTICES instead of chromedriver)
        # Check if the path ends with the wrong file
        if 'THIRD_PARTY_NOTICES' in driver_path or not driver_path.endswith(('chromedriver', 'chromedriver.exe')):
            logger.warning("Returned path is not a valid executable, searching for chromedriver...")
            driver_dir = os.path.dirname(driver_path)
            logger.info(f"Searching in directory: {driver_dir}")

            # Look for chromedriver in common locations
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
                logger.info(f"Glob pattern {pattern} found: {found}")

            # Find the first executable file
            for path in possible_paths:
                logger.info(f"Checking path: {path}")
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    driver_path = path
                    logger.info(f"Found valid chromedriver at: {driver_path}")
                    break
            else:
                logger.error(f"Could not find valid chromedriver in {driver_dir}")
                logger.error(f"Checked paths: {possible_paths}")

        logger.info(f"Using chromedriver at: {driver_path}")
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