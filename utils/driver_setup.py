# utils/driver_setup.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.os_manager import ChromeType
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
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

        # Ensure we're using the actual chromedriver executable, not a text file
        if not driver_path.endswith('chromedriver'):
            # Fix path if webdriver-manager returns wrong file
            import glob
            driver_dir = os.path.dirname(driver_path)
            chromedriver_files = glob.glob(os.path.join(driver_dir, '**/chromedriver'), recursive=True)
            if chromedriver_files:
                driver_path = chromedriver_files[0]

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