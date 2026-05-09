# utils/driver_setup.py
import os
import shutil
import glob
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from utils.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)

def _is_executable(path):
    """Check if path is a valid executable file."""
    return path and os.path.isfile(path) and os.access(path, os.X_OK)

def _find_chromedriver():
    """Find chromedriver with priority: env var > system PATH > webdriver-manager."""

    # 1. Explicit env override
    env_path = os.getenv("CHROMEDRIVER_PATH")
    if env_path and _is_executable(env_path):
        logger.info(f"Using CHROMEDRIVER_PATH env: {env_path}")
        return env_path

    # 2. System chromedriver on PATH (GitHub Actions installs this)
    system_path = shutil.which("chromedriver")
    if system_path and _is_executable(system_path):
        logger.info(f"Using system chromedriver: {system_path}")
        return system_path

    # 3. Fall back to webdriver-manager (local dev)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        wdm_path = ChromeDriverManager().install()
        logger.info(f"webdriver-manager returned: {wdm_path}")

        # Check if it's the actual binary
        if _is_executable(wdm_path) and not 'THIRD_PARTY_NOTICES' in wdm_path:
            return wdm_path

        # Search for the real binary in the same directory
        search_dir = os.path.dirname(wdm_path)
        logger.info(f"Searching for chromedriver in: {search_dir}")

        # Common locations
        candidates = [
            os.path.join(search_dir, 'chromedriver'),
            os.path.join(search_dir, 'chromedriver-linux64', 'chromedriver'),
            os.path.join(search_dir, 'chromedriver-mac-x64', 'chromedriver'),
            os.path.join(search_dir, 'chromedriver-win64', 'chromedriver.exe'),
        ]

        # Recursive search
        for pattern in ['**/chromedriver', '**/chromedriver.exe']:
            found = glob.glob(os.path.join(search_dir, pattern), recursive=True)
            candidates.extend(found)

        # Find first valid executable
        for candidate in candidates:
            if _is_executable(candidate):
                logger.info(f"Found valid chromedriver at: {candidate}")
                return candidate

        raise RuntimeError(f"No valid chromedriver found near {wdm_path}")

    except Exception as e:
        raise RuntimeError(f"Could not locate chromedriver: {e}")

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

        # Find chromedriver with proper priority
        driver_path = _find_chromedriver()
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