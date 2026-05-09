# pages/checkout_page.py
from pages.base_page import BasePage
from utils.config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class CheckoutLocators:
    BILLING_ADDR_SELECT  = (By.ID, "billing-address-select")
    BILLING_FIRSTNAME    = (By.ID, "BillingNewAddress_FirstName")
    BILLING_LASTNAME     = (By.ID, "BillingNewAddress_LastName")
    BILLING_EMAIL        = (By.ID, "BillingNewAddress_Email")
    BILLING_COUNTRY      = (By.ID, "BillingNewAddress_CountryId")
    BILLING_STATE        = (By.ID, "BillingNewAddress_StateProvinceId")
    BILLING_CITY         = (By.ID, "BillingNewAddress_City")
    BILLING_ADDRESS1     = (By.ID, "BillingNewAddress_Address1")
    BILLING_ZIP          = (By.ID, "BillingNewAddress_ZipPostalCode")
    BILLING_PHONE        = (By.ID, "BillingNewAddress_PhoneNumber")
    BILLING_CONTINUE     = (By.CSS_SELECTOR, "#opc-billing input.new-address-next-step-button")

    SHIPPING_CONTINUE    = (By.CSS_SELECTOR, "#opc-shipping input.new-address-next-step-button")

    ORDER_SUCCESS_MSG = (By.CSS_SELECTOR, ".section.order-completed div strong")
    ORDER_NUMBER      = (By.XPATH, "//div[contains(text(),'Order number')]")
    TERMS_CHECKBOX       = (By.ID, "termsofservice")
    CHECKOUT_BTN         = (By.ID, "checkout")


class CheckoutPage(BasePage):

    def open_cart(self):
        self.navigate(f"{BASE_URL}/cart")

    def _dismiss_alert(self):
        try:
            alert = self.driver.switch_to.alert
            print(f"\n→ Alert đóng: {alert.text}")
            alert.accept()
            self._pause(1)
        except:
            pass

    def _js_click_element(self, el):
        self.driver.execute_script("arguments[0].click();", el)

    def _js_set_value(self, locator, value):
        el = self.find(locator)
        self.driver.execute_script(
            "arguments[0].style.display='block';"
            "arguments[0].removeAttribute('disabled');"
            "arguments[0].value=arguments[1];",
            el, value
        )

    def _wait_section_active(self, section_id, timeout=15):
        """Chờ section có class active."""
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"#{section_id}.active")
            )
        )
        self._pause(1)

    # ── Step 0: Proceed to checkout ──────────────────────────
    def proceed_to_checkout(self):
        self.click(CheckoutLocators.TERMS_CHECKBOX)
        self._pause(0.5)
        self.click(CheckoutLocators.CHECKOUT_BTN)
        self._pause(2)

    # ── Step 1: Billing address ──────────────────────────────
    def fill_billing_us_address(self):
        try:
            dropdown = self.driver.find_elements(*CheckoutLocators.BILLING_ADDR_SELECT)
            if dropdown and dropdown[0].is_displayed():
                self.driver.execute_script(
                    "arguments[0].value='0';"
                    "arguments[0].dispatchEvent(new Event('change'));",
                    dropdown[0]
                )
                self._pause(2)
                print("\n→ Đã chọn New Address")
        except Exception as e:
            print(f"\n→ Dropdown lỗi: {e}")

        self._js_set_value(CheckoutLocators.BILLING_FIRSTNAME, "Test")
        self._js_set_value(CheckoutLocators.BILLING_LASTNAME,  "User")
        self._js_set_value(CheckoutLocators.BILLING_EMAIL,     "test@test.com")
        self._pause(0.5)

        try:
            select = Select(self.find(CheckoutLocators.BILLING_COUNTRY))
            select.select_by_value("1")
            self._pause(2)
            print("\n→ Đã chọn United States")
        except Exception as e:
            print(f"\n→ Country lỗi: {e}")

        try:
            state = Select(self.find(CheckoutLocators.BILLING_STATE))
            state.select_by_index(1)
            self._pause(0.5)
        except:
            pass

        self._js_set_value(CheckoutLocators.BILLING_CITY,     "New York")
        self._js_set_value(CheckoutLocators.BILLING_ADDRESS1, "123 Main St")
        self._js_set_value(CheckoutLocators.BILLING_ZIP,      "10001")
        self._js_set_value(CheckoutLocators.BILLING_PHONE,    "1234567890")
        self._pause(0.5)

    def continue_billing(self):
        el = self.find(CheckoutLocators.BILLING_CONTINUE)
        self._js_click_element(el)
        self._pause(4)
        self._dismiss_alert()

    # ── Step 2: Shipping address ─────────────────────────────
    def handle_shipping_address(self):
        """Chờ shipping address section active rồi click Continue."""
        try:
            self._wait_section_active("opc-shipping")
            print("\n→ Shipping Address section active")
            # Dùng địa chỉ saved có sẵn (US address vừa tạo) → click Continue luôn
            el = self.find(CheckoutLocators.SHIPPING_CONTINUE)
            self._js_click_element(el)
            self._pause(3)
            self._dismiss_alert()
            print("\n→ Đã continue Shipping Address")
        except Exception as e:
            print(f"\n→ Shipping Address lỗi: {e}")

    # ── Step 3: Shipping method ──────────────────────────────
    def select_shipping_method(self):
        self._dismiss_alert()
        try:
            self._wait_section_active("opc-shipping_method")
            methods = self.driver.find_elements(
                By.CSS_SELECTOR, "#opc-shipping_method input[type='radio']"
            )
            if methods:
                self._js_click_element(methods[0])
                print(f"\n→ Shipping method: {methods[0].get_attribute('value')}")
            else:
                print("\n→ Không tìm thấy shipping radio!")
        except Exception as e:
            print(f"\n→ Shipping method lỗi: {e}")
        self._pause(1)

    def continue_shipping_method(self):
        self._dismiss_alert()
        try:
            btn = self.driver.find_element(
                By.CSS_SELECTOR, "#opc-shipping_method input.button-1"
            )
            self._js_click_element(btn)
            self._pause(3)
        except Exception as e:
            print(f"\n→ Continue shipping lỗi: {e}")
        self._dismiss_alert()

    # ── Step 4: Payment method ───────────────────────────────
    def select_payment_method(self):
        self._dismiss_alert()
        try:
            self._wait_section_active("opc-payment_method")
            methods = self.driver.find_elements(
                By.CSS_SELECTOR, "#opc-payment_method input[type='radio']"
            )
            if methods:
                self._js_click_element(methods[0])
                print(f"\n→ Payment method: {methods[0].get_attribute('value')}")
        except Exception as e:
            print(f"\n→ Payment method lỗi: {e}")
        self._pause(1)

    def continue_payment_method(self):
        self._dismiss_alert()
        try:
            btn = self.driver.find_element(
                By.CSS_SELECTOR, "#opc-payment_method input.button-1"
            )
            self._js_click_element(btn)
            self._pause(3)
        except Exception as e:
            print(f"\n→ Continue payment lỗi: {e}")
        self._dismiss_alert()

    # ── Step 5: Payment info ─────────────────────────────────
    def fill_payment_info(self):
        """CashOnDelivery có thể không có payment info form — bỏ qua nếu không có."""
        self._dismiss_alert()
        try:
            # Chờ tối đa 5 giây — nếu không có thì bỏ qua
            from selenium.webdriver.support.ui import WebDriverWait
            short_wait = WebDriverWait(self.driver, 5)
            short_wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#opc-payment_info.active")
                )
            )
            self._pause(1)
            po = self.driver.find_elements(By.ID, "PurchaseOrderNumber")
            if po:
                po[0].clear()
                po[0].send_keys("PO-TEST-001")
                print("\n→ Điền PO number")
            else:
                print("\n→ Không có PO form — bỏ qua")
        except Exception as e:
            print(f"\n→ Payment info không có hoặc bỏ qua: {e}")
        self._pause(0.5)

    def continue_payment_info(self):
        """Chỉ click Continue nếu section payment_info đang active."""
        self._dismiss_alert()
        try:
            # Kiểm tra section có active không trước khi click
            active = self.driver.find_elements(
                By.CSS_SELECTOR, "#opc-payment_info.active"
            )
            if active:
                btn = self.driver.find_element(
                    By.CSS_SELECTOR, "#opc-payment_info input.button-1"
                )
                self._js_click_element(btn)
                self._pause(3)
                print("\n→ Đã continue payment info")
            else:
                print("\n→ Không có payment info step — bỏ qua")
        except Exception as e:
            print(f"\n→ Continue payment info lỗi: {e}")
        self._dismiss_alert()

    # ── Step 6: Confirm order ────────────────────────────────
    def confirm_order(self):
        self._dismiss_alert()
        self._pause(3)  # chờ thêm
        
        # Debug: in trạng thái tất cả sections
        sections = self.driver.find_elements(By.CSS_SELECTOR, "#checkout-steps li")
        print("\n--- Sections hiện tại ---")
        for s in sections:
            print(f"  id='{s.get_attribute('id')}' class='{s.get_attribute('class')}'")
        
        # Debug: in URL hiện tại
        print(f"\n→ URL: {self.driver.current_url}")
        
        # Thử click confirm không cần chờ active
        try:
            btns = self.driver.find_elements(
                By.CSS_SELECTOR, "#opc-confirm_order input[type='button']"
            )
            print(f"\n→ Confirm buttons tìm thấy: {len(btns)}")
            for btn in btns:
                print(f"  value='{btn.get_attribute('value')}' displayed='{btn.is_displayed()}'")
            if btns:
                self._js_click_element(btns[0])
                self._pause(3)
                print("\n→ Đã click confirm!")
        except Exception as e:
            print(f"\n→ Confirm lỗi: {e}")
        
        # Debug: kiểm tra order success
        success = self.driver.find_elements(
            By.CSS_SELECTOR, ".order-completed"
        )
        print(f"\n→ Order completed element: {len(success)}")
    def get_order_success_message(self):
        try:
            el = self.driver.find_element(
                By.CSS_SELECTOR, ".section.order-completed div strong"
            )
            return el.text
        except:
            try:
                # fallback
                el = self.driver.find_element(By.CSS_SELECTOR, ".title")
                return el.text
            except:
                return ""

    def get_order_number(self):
        try:
            # Tìm element chứa "Order number: XXXXXX"
            el = self.driver.find_element(
                By.XPATH, "//*[contains(text(),'Order number')]"
            )
            text = el.text  # "Order number: 2248612"
            return text.split(":")[-1].strip()  # "2248612"
        except:
            return ""

    def is_order_completed(self):
        try:
            # Kiểm tra URL chứa /completed/ hoặc element success
            if "completed" in self.driver.current_url:
                return True
            return self.is_visible((By.CSS_SELECTOR, ".section.order-completed"))
        except:
            return False
    # ── Full checkout flow ───────────────────────────────────
    def do_full_checkout(self):
        self.proceed_to_checkout()
        self.fill_billing_us_address()
        self.continue_billing()
        self.handle_shipping_address()   # ← thêm step này
        self.select_shipping_method()
        self.continue_shipping_method()
        self.select_payment_method()
        self.continue_payment_method()
        self.fill_payment_info()
        self.continue_payment_info()
        self.confirm_order()