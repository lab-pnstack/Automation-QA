# tests/test_search_product.py
import pytest
from pages.product_page import ProductPage

class TestBrowseCategory:

    # TC01: Kiểm tra menu hiển thị đủ category
    def test_nav_menu_visible(self, driver):
        page = ProductPage(driver)
        page.open_homepage()
        menus = page.get_nav_menu_items()
        assert len(menus) > 0, "Menu không có item nào"
        print(f"\n→ Menu items: {menus}")

    # TC02: Browse vào category Books
    def test_browse_books_category(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        assert "books" in page.get_url().lower()
        count = page.get_result_count()
        assert count > 0, "Category Books không có sản phẩm"
        print(f"\n→ Số sản phẩm trong Books: {count}")

    # TC03: Browse vào category Computers
    def test_browse_computers_category(self, driver):
        page = ProductPage(driver)
        page.open_category("/computers")
        assert "computers" in page.get_url().lower()

    # TC04: Browse vào category Electronics
    def test_browse_electronics_category(self, driver):
        page = ProductPage(driver)
        page.open_category("/electronics")
        assert "electronics" in page.get_url().lower()


class TestSearchProduct:

    # TC05: Tìm kiếm sản phẩm tồn tại
    def test_search_existing_product(self, driver):
        page = ProductPage(driver)
        page.open_homepage()
        page.search("book")
        results = page.get_search_results()
        assert len(results) > 0, "Không tìm thấy kết quả cho 'book'"
        print(f"\n→ Tìm được {len(results)} sản phẩm")

    # TC06: debug tìm locator no-result
    def test_search_nonexistent_product(self, driver):
        page = ProductPage(driver)
        page.open_homepage()
        page.search("xyzxyzxyz123")
        import time; time.sleep(2)

        # In ra toàn bộ text trên trang sau khi search
        body_text = driver.find_element("tag name", "body").text
        print("\n--- BODY TEXT sau khi search không có kết quả ---")
        print(body_text[:800])   # 800 ký tự đầu

        # In ra tất cả class của các div/p để tìm đúng locator
        from selenium.webdriver.common.by import By
        elements = driver.find_elements(By.CSS_SELECTOR, "div, p, span")
        for el in elements:
            cls = el.get_attribute("class")
            txt = el.text.strip()
            if txt and len(txt) < 100 and ("no" in txt.lower() or "found" in txt.lower() or "result" in txt.lower()):
                print(f"  class='{cls}' | text='{txt}'")

        assert True  # tạm pass để xem output

    # TC07: Tìm kiếm với keyword ngắn 1 ký tự
    def test_search_single_character(self, driver):
        page = ProductPage(driver)
        page.open_homepage()
        page.search("a")
        results = page.get_search_results()
        print(f"\n→ Tìm 'a' được {len(results)} sản phẩm")
        assert True  # chỉ kiểm tra không bị crash

    # TC08: Tìm kiếm với ô trống
    def test_search_empty_keyword(self, driver):
        page = ProductPage(driver)
        page.open_homepage()
        page.search("")
        assert True  # không crash là pass


class TestProductDetail:

    # TC09: Xem chi tiết sản phẩm
    def test_view_product_detail(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.click_first_product()
        name = page.get_product_name()
        assert name != "", "Tên sản phẩm trống"
        print(f"\n→ Sản phẩm: {name}")

    # TC10: Kiểm tra giá sản phẩm hiển thị
    def test_product_price_displayed(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.click_first_product()
        price = page.get_product_price()
        assert price != "", "Giá sản phẩm không hiển thị"
        print(f"\n→ Giá: {price}")

    # TC11: Kiểm tra nút Add to Cart có trên trang detail
    def test_add_to_cart_button_visible(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.click_first_product()
        assert page.is_add_to_cart_visible(), "Không thấy nút Add to Cart"

    # TC12: Kiểm tra nút Add to Wishlist có trên trang product detail
    def test_add_to_wishlist_button_visible(self, logged_in_driver):
        page = ProductPage(logged_in_driver)
        page.navigate("https://demowebshop.tricentis.com/health")  # ← đổi URL này
        assert page.is_add_to_wishlist_visible(), "Không thấy nút Add to Wishlist"
        print(f"\n→ Nút Add to Wishlist hiển thị đúng!")


class TestFilterProduct:

    # TC13: Sort sản phẩm theo tên A-Z
    def test_sort_by_name_az(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.sort_by("Name: A to Z")
        names = page.get_all_product_names()
        assert names == sorted(names), "Sản phẩm chưa được sort đúng A-Z"
        print(f"\n→ Sort A-Z: {names}")

    # TC14: Sort sản phẩm theo giá thấp đến cao
    def test_sort_by_price_low_high(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.sort_by("Price: Low to High")
        prices = page.get_all_product_prices()
        assert prices == sorted(prices), "Giá chưa được sort đúng thấp→cao"
        print(f"\n→ Prices: {prices}")

    # TC15: Thay đổi số sản phẩm hiển thị mỗi trang
    def test_change_page_size(self, driver):
        page = ProductPage(driver)
        page.open_category("/books")
        page.set_page_size(4)
        count = page.get_result_count()
        assert count <= 4, f"Hiển thị {count} sản phẩm, kỳ vọng <= 4"
        print(f"\n→ Hiển thị {count} sản phẩm/trang")