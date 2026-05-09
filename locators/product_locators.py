# locators/product_locators.py
from selenium.webdriver.common.by import By

class ProductLocators:
    # Navigation menu
    NAV_MENU_ITEMS    = (By.CSS_SELECTOR, "ul.top-menu > li > a")
    CATEGORY_BOOKS    = (By.CSS_SELECTOR, "a[href='/books']")
    CATEGORY_COMPUTERS = (By.CSS_SELECTOR, "a[href='/computers']")
    CATEGORY_ELECTRONICS = (By.CSS_SELECTOR, "a[href='/electronics']")

    # Search
    SEARCH_INPUT      = (By.ID, "small-searchterms")
    SEARCH_BUTTON     = (By.CSS_SELECTOR, "input.search-box-button")
    SEARCH_RESULTS    = (By.CSS_SELECTOR, ".product-item")
    SEARCH_NO_RESULT = (By.CSS_SELECTOR, "strong.result")
    RESULT_COUNT      = (By.CSS_SELECTOR, ".product-selectors span")

    # Product list
    PRODUCT_TITLES    = (By.CSS_SELECTOR, ".product-title a")
    PRODUCT_PRICES    = (By.CSS_SELECTOR, ".price.actual-price")
    FIRST_PRODUCT     = (By.CSS_SELECTOR, ".product-item:first-child .product-title a")
    PRODUCT_GRID_ITEMS = (By.CSS_SELECTOR, ".item-box")

    # Product detail
    PRODUCT_NAME      = (By.CSS_SELECTOR, ".product-name h1")
    PRODUCT_PRICE     = (By.CSS_SELECTOR, ".product-price span")
    PRODUCT_SKU       = (By.CSS_SELECTOR, ".sku .value")
    PRODUCT_DESC      = (By.CSS_SELECTOR, ".full-description")
    ADD_TO_CART_BTN   = (By.CSS_SELECTOR, "input.add-to-cart-button")
    ADD_TO_WISHLIST   = (By.CSS_SELECTOR, "input.add-to-wishlist-button")
    PRODUCT_IMAGES    = (By.CSS_SELECTOR, ".picture img")

    # Filter / Sort
    SORT_DROPDOWN     = (By.ID, "products-orderby")
    PAGE_SIZE_SELECT  = (By.ID, "products-pagesize")
    PRICE_RANGE_FROM  = (By.CSS_SELECTOR, "input.from")
    PRICE_RANGE_TO    = (By.CSS_SELECTOR, "input.to")
    FILTER_APPLY      = (By.CSS_SELECTOR, "input.price-range-go")

    # Breadcrumb
    BREADCRUMB        = (By.CSS_SELECTOR, ".breadcrumb li")