# locators/cart_locators.py
from selenium.webdriver.common.by import By

class CartLocators:
    # Add to cart
    ADD_TO_CART_BTN      = (By.CSS_SELECTOR, "input.add-to-cart-button")
    QTY_INPUT            = (By.CSS_SELECTOR, "input.qty-input")
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, "p.content")

    # Cart page
    CART_LINK            = (By.CSS_SELECTOR, "a[href='/cart']")
    CART_PAGE_ITEMS      = (By.CSS_SELECTOR, "tr.cart-item-row")
    CART_QTY_INPUTS      = (By.CSS_SELECTOR, "input.qty-input")
    CART_ITEM_NAMES      = (By.CSS_SELECTOR, "td.product .product-name")
    CART_ITEM_PRICES     = (By.CSS_SELECTOR, "td.unit-price .product-unit-price")
    CART_SUBTOTALS       = (By.CSS_SELECTOR, "td.subtotal .product-subtotal")
    CART_TOTAL           = (By.CSS_SELECTOR, "td[class='cart-total-right'] span.value-summary strong")
    EMPTY_CART_MSG       = (By.CSS_SELECTOR, ".order-summary-content .no-data")

    # Update / Remove  ← SỬA 2 DÒNG NÀY
    UPDATE_CART_BTN      = (By.CSS_SELECTOR, "input[name='updatecart']")
    REMOVE_CHECKBOX      = (By.CSS_SELECTOR, "input[name='removefromcart']")  # ← SỬA
    REMOVE_ALL_CHECKBOX  = (By.CSS_SELECTOR, "input[name='removefromcart']")  # ← SỬA

    # Checkout
    CHECKOUT_BTN         = (By.ID, "checkout")
    TERMS_CHECKBOX       = (By.ID, "termsofservice")