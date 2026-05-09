# utils/config.py

BASE_URL = "https://demowebshop.tricentis.com"

# Tài khoản test (tạo sẵn trên web)
TEST_EMAIL    = "anhlinh@gmail.com"
TEST_PASSWORD = "Maclang23."

# Browser settings
BROWSER      = "chrome"      # hoặc "firefox"
HEADLESS     = False          # True = chạy ẩn (không mở cửa sổ)
IMPLICIT_WAIT = 2            # giây
PAGE_LOAD_TIMEOUT = 30

# Đường dẫn output
SCREENSHOT_DIR = "screenshots/"
REPORT_DIR     = "reports/"

SLOW_MODE       = True   # True = chạy chậm cho demo
STEP_DELAY      = 0.5    # Giây dừng giữa mỗi thao tác
ACTION_DELAY    = 0.5    # Giây dừng sau mỗi click/type