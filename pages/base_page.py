# pages/base_page.py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import SLOW_MODE, ACTION_DELAY, STEP_DELAY

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def _pause(self, seconds=None):
        """Dừng lại để demo — chỉ active khi SLOW_MODE = True."""
        if SLOW_MODE:
            time.sleep(seconds or ACTION_DELAY)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self._pause()          # dừng trước khi click
        element.click()
        self._pause()          # dừng sau khi click

    def type(self, locator, text):
        el = self.find(locator)
        self._pause(0.5)
        el.clear()
        # Gõ từng ký tự cho có cảm giác đang nhập thật
        if SLOW_MODE:
            for char in text:
                el.send_keys(char)
                time.sleep(0.07)
        else:
            el.send_keys(text)
        self._pause(0.5)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def get_url(self):
        return self.driver.current_url

    def navigate(self, url):
        self.driver.get(url)
        self._pause(STEP_DELAY)   # chờ trang load xong mới làm tiếp