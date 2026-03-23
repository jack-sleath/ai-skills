#!/usr/bin/env python3
"""
Load the Claude usage page in Chrome (using an existing profile) and
return the rendered page content for downstream processing.

Usage:
    python tools/read_usage.py                          # auto-detect Chrome profile
    python tools/read_usage.py --profile-dir "Profile 1"  # specific profile
    python tools/read_usage.py --user-data-dir /path/to/chrome/user-data
    python tools/read_usage.py --html                   # include rendered HTML as well as text
"""

import argparse
import json
import os
import platform
import sys
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    sys.exit(
        "selenium is required. Install it with:\n"
        "  pip install selenium\n"
        "You also need chromedriver — see https://chromedriver.chromium.org/downloads"
    )

USAGE_URL = "https://claude.ai/settings/usage"
ELEMENT_WAIT_TIMEOUT = 15


def default_chrome_user_data_dir() -> str:
    """Return the default Chrome user-data directory for this platform."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data")
    elif system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    else:  # Linux
        return os.path.expanduser("~/.config/google-chrome")


def build_driver(user_data_dir: str, profile_dir: str, headless: bool = False) -> webdriver.Chrome:
    """Create a Chrome WebDriver attached to an existing profile."""
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")

    if headless:
        options.add_argument("--headless=new")

    # Suppress noisy logging
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(options=options)


def fetch_usage_page(driver: webdriver.Chrome, include_html: bool = False) -> dict:
    """Navigate to the usage page and return the rendered content."""
    driver.get(USAGE_URL)

    wait = WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    # Give JS frameworks a moment to render
    time.sleep(2)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    result = {
        "url": USAGE_URL,
        "page_text": page_text,
        "status": "ok" if page_text.strip() else "empty",
    }

    if include_html:
        main_el = driver.find_element(By.TAG_NAME, "main")
        result["page_html"] = main_el.get_attribute("outerHTML")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch the Claude usage page and return its rendered content"
    )
    parser.add_argument(
        "--user-data-dir",
        default=None,
        help="Chrome user-data directory (default: auto-detect)",
    )
    parser.add_argument(
        "--profile-dir",
        default="Default",
        help="Chrome profile directory name (default: 'Default')",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode (may not work if login cookies require visible browser)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        dest="include_html",
        help="Include the rendered HTML of the <main> element in the output",
    )
    args = parser.parse_args()

    user_data_dir = args.user_data_dir or default_chrome_user_data_dir()

    if not os.path.isdir(user_data_dir):
        sys.exit(f"Chrome user-data directory not found: {user_data_dir}")

    driver = None
    try:
        driver = build_driver(user_data_dir, args.profile_dir, headless=args.headless)
        result = fetch_usage_page(driver, include_html=args.include_html)
    except Exception as e:
        result = {"status": "error", "error": str(e)}
    finally:
        if driver:
            driver.quit()

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("status") == "ok" else 1)


if __name__ == "__main__":
    main()
