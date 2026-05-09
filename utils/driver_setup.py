# utils/driver_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from utils.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

CHROME_DRIVER_PATH = r"D:\TEST\drivers\chromedriver.exe"

def get_driver():
    if BROWSER.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=ChromeService(CHROME_DRIVER_PATH),
            options=options
        )
    else:
        raise ValueError(f"Browser '{BROWSER}' không được hỗ trợ.")

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver