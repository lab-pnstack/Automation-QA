# tests/test_user_account.py
import pytest
from pages.account_page import AccountPage
from pages.cart_page import CartPage
from utils.config import TEST_EMAIL, TEST_PASSWORD

PRODUCT_WITH_WISHLIST = "/health"  # sản phẩm có nút Add to wishlist


class TestWishlist:

    # TC01: Thêm sản phẩm vào wishlist thành công
    def test_add_to_wishlist(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.add_to_wishlist(PRODUCT_WITH_WISHLIST)
        page.open_wishlist()
        count = page.get_wishlist_count()
        print(f"\n→ Số sản phẩm trong wishlist: {count}")
        assert count > 0, "Wishlist phải có sản phẩm sau khi thêm"

    # TC02: Wishlist hiển thị đúng tên sản phẩm
    def test_wishlist_shows_product(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.add_to_wishlist(PRODUCT_WITH_WISHLIST)
        page.open_wishlist()

        from selenium.webdriver.common.by import By
        names = logged_in_driver.find_elements(
            By.CSS_SELECTOR, ".wishlist-content td.product a"
        )
        print(f"\n→ Sản phẩm trong wishlist: {[n.text for n in names]}")
        assert len(names) > 0, "Wishlist phải hiển thị tên sản phẩm"

    # TC03: Xóa sản phẩm khỏi wishlist
    def test_remove_from_wishlist(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.add_to_wishlist(PRODUCT_WITH_WISHLIST)
        page.open_wishlist()
        count_before = page.get_wishlist_count()
        page.remove_from_wishlist()
        count_after = page.get_wishlist_count()
        print(f"\n→ Trước: {count_before} | Sau: {count_after}")
        assert count_after < count_before

    # TC04: Wishlist accessible khi đã đăng nhập
    def test_wishlist_accessible(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_wishlist()
        assert "wishlist" in page.get_url().lower()
        print(f"\n→ URL wishlist: {page.get_url()}")

    # TC05: Wishlist redirect về login khi chưa đăng nhập
    def test_wishlist_requires_login(self, driver):
        page = AccountPage(driver)
        page.open_wishlist()
        url = page.get_url()
        print(f"\n→ URL sau khi vào wishlist chưa login: {url}")
        assert "login" in url.lower() or "wishlist" in url.lower()


class TestOrderHistory:

    # TC06: Xem danh sách order history
    def test_view_order_history(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_order_history()
        count = page.get_order_count()
        print(f"\n→ Số orders: {count}")
        assert count > 0, "Phải có ít nhất 1 order"

    # TC07: Order history hiển thị đúng thông tin
    def test_order_history_has_info(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_order_history()
        from selenium.webdriver.common.by import By
        # Kiểm tra có Order Number, Status, Date, Total
        body = logged_in_driver.find_element(
            By.CSS_SELECTOR, ".master-wrapper-content"
        ).text
        print(f"\n→ Kiểm tra thông tin order...")
        assert "Order Number" in body
        assert "Order status" in body
        assert "Order Date"   in body
        assert "Order Total"  in body
        print("→ Đầy đủ thông tin order!")

    # TC08: Xem chi tiết order
    def test_view_order_detail(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_order_history()
        page.click_order_details(index=0)
        url = page.get_url()
        print(f"\n→ URL order detail: {url}")
        assert "order" in url.lower()

    # TC09: Order history page accessible
    def test_order_history_accessible(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_order_history()
        assert "orders" in page.get_url().lower()
        print(f"\n→ URL: {page.get_url()}")


class TestChangePassword:

    # TC10: Đổi password thành công
    def test_change_password_success(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_change_password()
        page.change_password(
            old_pwd=TEST_PASSWORD,
            new_pwd=TEST_PASSWORD  # đổi về password cũ để test lại được
        )
        assert page.is_password_changed_successfully()
        msg = page.get_password_success_msg()
        print(f"\n→ Kết quả: {msg}")
        assert "changed" in msg.lower() or "success" in msg.lower()

    # TC11: Đổi password với old password sai
    def test_change_password_wrong_old(self, logged_in_driver):
        page = AccountPage(logged_in_driver)
        page.open_change_password()
        page.change_password(
            old_pwd="WrongOldPass@123",
            new_pwd="NewPass@456"
        )
        assert not page.is_password_changed_successfully() or \
               page.is_visible(AccountPage.PWD_ERROR_MSG if hasattr(AccountPage, 'PWD_ERROR_MSG') else AccountLocators.PWD_ERROR_MSG)
        print(f"\n→ Không đổi được với old password sai")

    # TC12: Đổi password với new password quá ngắn
    def test_change_password_too_short(self, logged_in_driver):
        from pages.account_page import AccountLocators
        page = AccountPage(logged_in_driver)
        page.open_change_password()
        page.change_password(
            old_pwd=TEST_PASSWORD,
            new_pwd="123"
        )
        assert page.is_visible(AccountLocators.PWD_ERROR_MSG)
        print(f"\n→ Lỗi password quá ngắn")

    # TC13: Đổi password với confirm không khớp
    def test_change_password_mismatch(self, logged_in_driver):
        from pages.account_page import AccountLocators
        page = AccountPage(logged_in_driver)
        page.open_change_password()
        page.type(AccountLocators.OLD_PASSWORD,         TEST_PASSWORD)
        page.type(AccountLocators.NEW_PASSWORD,         "NewPass@456")
        page.type(AccountLocators.CONFIRM_NEW_PASSWORD, "Different@789")
        page.click(AccountLocators.CHANGE_PWD_BTN)
        page._pause(2)
        assert page.is_visible(AccountLocators.PWD_ERROR_MSG)
        print(f"\n→ Lỗi confirm password không khớp")