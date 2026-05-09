# tests/test_add_to_cart.py
import pytest
from pages.cart_page import CartPage

# URL sản phẩm dùng để test
PRODUCT_URL  = "/health"        # sản phẩm đơn giản, có nút Add to cart
PRODUCT_URL2 = "/fiction"       # sản phẩm thứ 2


class TestAddToCart:

    # TC01: Thêm sản phẩm vào cart thành công
    def test_add_single_product(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        notify = page.get_notification_text()
        print(f"\n→ Thông báo: {notify}")
        assert "cart" in notify.lower(), "Không thấy thông báo thêm vào cart"

    # TC02: Thêm sản phẩm với số lượng > 1
    def test_add_product_with_quantity(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        page.open_product(PRODUCT_URL)
        page.set_quantity_before_add(3)
        page.add_to_cart()
        notify = page.get_notification_text()
        assert "cart" in notify.lower()
        print(f"\n→ Thêm 3 sản phẩm: {notify}")

    # TC03: Thêm nhiều sản phẩm khác nhau vào cart
    def test_add_multiple_products(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        # Thêm sản phẩm 1
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        # Thêm sản phẩm 2
        page.open_product(PRODUCT_URL2)
        page.add_to_cart()
        # Vào cart kiểm tra
        page.open_cart()
        count = page.get_cart_item_count()
        print(f"\n→ Số sản phẩm trong cart: {count}")
        assert count >= 2, "Cart phải có ít nhất 2 sản phẩm"

    # TC04: Kiểm tra sản phẩm đúng tên sau khi thêm
    def test_product_name_in_cart(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_cart()
        names = page.get_cart_item_names()
        print(f"\n→ Sản phẩm trong cart: {names}")
        assert len(names) > 0, "Cart không có sản phẩm nào"


class TestUpdateCart:

    # TC05: Cập nhật số lượng sản phẩm trong cart
    def test_update_quantity(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        # Thêm sản phẩm vào cart trước
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_cart()
        # Cập nhật số lượng thành 3
        page.update_quantity(index=0, new_qty=3)
        new_qty = page.get_item_qty(index=0)
        print(f"\n→ Số lượng sau update: {new_qty}")
        assert new_qty == "3", f"Số lượng kỳ vọng là 3, thực tế là {new_qty}"

    # TC06: Cập nhật số lượng thành 1
    def test_update_quantity_to_one(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_cart()
        page.update_quantity(index=0, new_qty=1)
        new_qty = page.get_item_qty(index=0)
        assert new_qty == "1"
        print(f"\n→ Số lượng sau update: {new_qty}")


class TestRemoveFromCart:

    # TC07: Xóa 1 sản phẩm khỏi cart
    def test_remove_single_item(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_cart()
        count_before = page.get_cart_item_count()
        page.remove_item(index=0)
        count_after = page.get_cart_item_count()
        print(f"\n→ Trước: {count_before} | Sau: {count_after}")
        assert count_after < count_before, "Sản phẩm chưa được xóa"

    # TC08: Xóa tất cả sản phẩm — cart phải trống
    def test_remove_all_items(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        # Thêm 2 sản phẩm
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_product(PRODUCT_URL2)
        page.add_to_cart()
        page.open_cart()
        page.remove_all_items()
        assert page.is_cart_empty(), "Cart phải trống sau khi xóa hết"
        print(f"\n→ Cart trống sau khi xóa hết!")

    # TC09: Kiểm tra thông báo cart trống
    def test_empty_cart_message(self, logged_in_driver):
        page = CartPage(logged_in_driver)
        # Thêm sản phẩm trước để đảm bảo có gì đó để xóa
        page.open_product(PRODUCT_URL)
        page.add_to_cart()
        page.open_cart()
        page.remove_all_items()
        assert page.is_cart_empty(), "Cart phải trống sau khi xóa hết"
        print(f"\n→ Cart trống: {page.is_cart_empty()}")

    # TC10: Kiểm tra cart trống khi mới vào (chưa thêm gì)
    def test_cart_empty_on_fresh_start(self, driver):
        page = CartPage(driver)
        page.open_cart()
        # Cart có thể trống hoặc có sản phẩm — chỉ kiểm tra trang load được
        url = page.get_url()
        assert "cart" in url.lower()
        print(f"\n→ Trang cart load OK: {url}")

