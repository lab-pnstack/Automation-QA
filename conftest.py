# conftest.py

import os
import json
import uuid
import pytest

from datetime import datetime

from utils.driver_setup import get_driver
from utils.config import BASE_URL


# =========================================================
# GLOBALS
# =========================================================

RUN_ID = (
    datetime.now().strftime("%Y%m%d_%H%M%S")
    + "_"
    + str(uuid.uuid4())[:4]
)

_results = []


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture(scope="function")
def driver():
    drv = get_driver()

    drv.get(BASE_URL)

    yield drv

    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    from pages.login_page import LoginPage
    from utils.config import TEST_EMAIL, TEST_PASSWORD

    login = LoginPage(driver)

    login.open()
    login.login(TEST_EMAIL, TEST_PASSWORD)

    yield driver


# =========================================================
# PYTEST REPORT HOOK
# =========================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    # =====================================================
    # Chỉ lấy setup + call
    # setup fail = ERROR
    # call fail  = FAILED
    # =====================================================

    if rep.when not in ["setup", "call"]:
        return

    # =====================================================
    # MODULE MAPPING
    # =====================================================

    file_name = ""

    if hasattr(item, "fspath"):
        file_name = item.fspath.basename.replace(".py", "")

    module_map = {
        "test_login": "Authentication",
        "test_register": "Authentication",
        "test_search_product": "Product",
        "test_add_to_cart": "Cart",
        "test_checkout": "Checkout",
        "test_user_account": "User Account",
    }

    module = module_map.get(file_name, "Other")

    # =====================================================
    # STATUS
    # =====================================================

    if rep.passed:
        status = "pass"

    elif rep.skipped:
        status = "skip"

    else:
        # setup crash => ERROR
        if rep.when == "setup":
            status = "error"

        # assertion fail / selenium fail in test body
        else:
            status = "fail"

    # =====================================================
    # ERROR MESSAGE
    # =====================================================

    error_msg = ""

    if rep.failed and rep.longrepr:
        error_msg = str(rep.longrepr)[-1500:]

    # =====================================================
    # DURATION
    # =====================================================

    duration = round(rep.duration, 2)

    # =====================================================
    # TEST INFO
    # =====================================================

    result = {
        "name": item.name,
        "node_id": item.nodeid,
        "module": module,
        "class": item.cls.__name__ if item.cls else "",
        "status": status,
        "duration": duration,
        "error": error_msg,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # =====================================================
    # SCREENSHOT WHEN FAIL / ERROR
    # =====================================================

    if status in ["fail", "error"]:

        drv = (
            item.funcargs.get("driver")
            or item.funcargs.get("logged_in_driver")
        )

        if drv:

            os.makedirs("screenshots", exist_ok=True)

            screenshot_path = (
                f"screenshots/{item.name}_{RUN_ID}.png"
            )

            try:
                drv.save_screenshot(screenshot_path)

                result["screenshot"] = screenshot_path

            except Exception:
                pass

    # =====================================================
    # AVOID DUPLICATE
    # setup fail rồi thì call sẽ skip
    # chỉ lưu 1 lần
    # =====================================================

    existing = next(
        (
            r for r in _results
            if r["node_id"] == item.nodeid
        ),
        None
    )

    if existing:

        # Ưu tiên error > fail > pass
        priority = {
            "error": 3,
            "fail": 2,
            "skip": 1,
            "pass": 0,
        }

        if priority[status] > priority[existing["status"]]:
            existing.update(result)

    else:
        _results.append(result)


# =========================================================
# SESSION FINISH
# =========================================================

def pytest_sessionfinish(session, exitstatus):

    if not _results:
        return

    os.makedirs("reports/history", exist_ok=True)

    # =====================================================
    # SUMMARY
    # =====================================================

    passed = sum(
        1 for r in _results
        if r["status"] == "pass"
    )

    failed = sum(
        1 for r in _results
        if r["status"] == "fail"
    )

    errors = sum(
        1 for r in _results
        if r["status"] == "error"
    )

    skipped = sum(
        1 for r in _results
        if r["status"] == "skip"
    )

    total = len(_results)

    total_duration = round(
        sum(r.get("duration", 0) for r in _results),
        2
    )

    pass_rate = (
        round((passed / total) * 100, 1)
        if total > 0
        else 0
    )

    # =====================================================
    # RUN DATA
    # =====================================================

    run_data = {
        "run_id": RUN_ID,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "total": total,
        "passed": passed,
        "failed": failed,
        "warning": 0,
        "error": errors,
        "skipped": skipped,
        "duration": total_duration,
        "pass_rate": pass_rate,
        "tests": _results,
    }

    # =====================================================
    # SAVE DETAIL FILE
    # =====================================================

    report_path = (
        f"reports/history/{RUN_ID}.json"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            run_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    # =====================================================
    # UPDATE INDEX
    # =====================================================

    index_path = "reports/history/index.json"

    index = []

    if os.path.exists(index_path):

        try:
            with open(
                index_path,
                "r",
                encoding="utf-8"
            ) as f:

                index = json.load(f)

        except Exception:
            index = []

    index.insert(0, {
        "run_id": RUN_ID,
        "date": run_data["date"],
        "total": total,
        "passed": passed,
        "failed": failed,
        "warning": 0,
        "error": errors,
        "skipped": skipped,
        "duration": total_duration,
        "pass_rate": pass_rate,
        "file": report_path,
    })

    with open(
        index_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            index,
            f,
            ensure_ascii=False,
            indent=2
        )

    # =====================================================
    # CONSOLE
    # =====================================================

    print("\n======================================")
    print("TEST EXECUTION SUMMARY")
    print("======================================")

    print(f"Run ID     : {RUN_ID}")
    print(f"Total      : {total}")
    print(f"Passed     : {passed}")
    print(f"Failed     : {failed}")
    print(f"Errors     : {errors}")
    print(f"Skipped    : {skipped}")
    print(f"Pass Rate  : {pass_rate}%")
    print(f"Duration   : {total_duration}s")

    print("======================================")

    print(f"\n✅ Report saved: {report_path}")