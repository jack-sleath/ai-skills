#!/usr/bin/env python3
"""
Read Claude usage percentage and next reset time from
https://claude.ai/settings/usage using Selenium with an existing Chrome profile.

Usage:
    python tools/read_usage.py                          # auto-detect Chrome profile
    python tools/read_usage.py --profile-dir "Profile 1"  # specific profile
    python tools/read_usage.py --user-data-dir /path/to/chrome/user-data
    python tools/read_usage.py --json                   # machine-readable output
"""

import argparse
import json
import os
import platform
import re
import sys
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
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
PAGE_LOAD_TIMEOUT = 30
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


def extract_reset_time(page_text: str, driver: webdriver.Chrome) -> str | None:
    """Try to find the next usage reset / renewal time from the page."""
    # Common patterns: "Resets in 3h 42m", "Resets at 2:00 PM",
    # "Next reset: March 24, 2026", "Usage resets in 3 hours",
    # "Your usage will reset in ...", "Renews in ..."
    reset_patterns = [
        r"(?:resets?|renews?|refreshes?)\s+(?:in|at)\s+(.+?)(?:\.|$)",
        r"(?:next\s+(?:reset|renewal|refresh))\s*[:\-]\s*(.+?)(?:\.|$)",
        r"(?:usage\s+(?:will\s+)?(?:reset|renew|refresh))\s+(?:in|at|on)\s+(.+?)(?:\.|$)",
        r"(?:limit\s+(?:will\s+)?(?:reset|renew|refresh))\s+(?:in|at|on)\s+(.+?)(?:\.|$)",
    ]

    for pattern in reset_patterns:
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Try to find a time element with a datetime attribute near reset-related text
    try:
        time_els = driver.find_elements(By.TAG_NAME, "time")
        for el in time_els:
            dt = el.get_attribute("datetime")
            if dt:
                return dt
    except Exception:
        pass

    # Try to find elements with reset-related aria-labels or titles
    try:
        for selector in [
            "[aria-label*='reset']", "[aria-label*='renew']",
            "[title*='reset']", "[title*='renew']",
        ]:
            els = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in els:
                label = el.get_attribute("aria-label") or el.get_attribute("title") or ""
                if label:
                    return label.strip()
    except Exception:
        pass

    return None


def extract_usage(driver: webdriver.Chrome) -> dict:
    """Navigate to the usage page and extract the percentage remaining and reset time."""
    driver.get(USAGE_URL)

    wait = WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT)

    # Wait for the page to have meaningful content loaded
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    # Give JS frameworks a moment to render
    time.sleep(2)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    result = {
        "url": USAGE_URL,
        "raw_text": None,
        "percentage_used": None,
        "percentage_remaining": None,
        "reset_time": None,
        "status": "unknown",
    }

    # --- Extract reset / next session time ---
    result["reset_time"] = extract_reset_time(page_text, driver)

    # --- Extract usage percentage ---
    # Common patterns: "X% used", "X% remaining", or a progress/meter element
    percentage_patterns = [
        r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(?:usage|limit|quota)?\s*used",
        r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(?:usage|limit|quota)?\s*remaining",
        r"(\d+(?:\.\d+)?)\s*%",
    ]

    for pattern in percentage_patterns:
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            matched_text = match.group(0).lower()
            result["raw_text"] = match.group(0)

            if "remaining" in matched_text:
                result["percentage_remaining"] = value
                result["percentage_used"] = round(100 - value, 2)
            else:
                result["percentage_used"] = value
                result["percentage_remaining"] = round(100 - value, 2)

            result["status"] = "ok"
            break

    # If no percentage found, try to grab any progress bar value
    if result["status"] == "unknown":
        try:
            progress_els = driver.find_elements(By.CSS_SELECTOR, "[role='progressbar'], progress, meter")
            for el in progress_els:
                val = el.get_attribute("value") or el.get_attribute("aria-valuenow")
                if val:
                    value = float(val)
                    # Normalise to percentage if it looks like a 0-1 range
                    if value <= 1:
                        value = value * 100
                    result["percentage_used"] = round(value, 2)
                    result["percentage_remaining"] = round(100 - value, 2)
                    result["status"] = "ok"
                    break
        except Exception:
            pass

    # If still nothing, try aria-label or title attributes on any bar-like element
    if result["status"] == "unknown":
        try:
            bar_els = driver.find_elements(By.CSS_SELECTOR, "[aria-label*='%'], [title*='%']")
            for el in bar_els:
                label = el.get_attribute("aria-label") or el.get_attribute("title") or ""
                match = re.search(r"(\d+(?:\.\d+)?)\s*%", label)
                if match:
                    result["raw_text"] = label
                    result["percentage_used"] = float(match.group(1))
                    result["percentage_remaining"] = round(100 - float(match.group(1)), 2)
                    result["status"] = "ok"
                    break
        except Exception:
            pass

    # If we found reset_time but not percentage, still mark partial success
    if result["status"] == "unknown" and result["reset_time"]:
        result["status"] = "partial"

    if result["status"] == "unknown":
        # Capture a snippet of the page for debugging
        snippet = page_text[:500] if page_text else "(empty page)"
        result["debug_snippet"] = snippet
        result["status"] = "not_found"

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Read Claude usage percentage from the web UI")
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
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result as JSON",
    )
    args = parser.parse_args()

    user_data_dir = args.user_data_dir or default_chrome_user_data_dir()

    if not os.path.isdir(user_data_dir):
        sys.exit(f"Chrome user-data directory not found: {user_data_dir}")

    driver = None
    try:
        driver = build_driver(user_data_dir, args.profile_dir, headless=args.headless)
        result = extract_usage(driver)
    except Exception as e:
        result = {"status": "error", "error": str(e)}
    finally:
        if driver:
            driver.quit()

    if args.json_output:
        # Drop debug_snippet from JSON if present — keep it clean
        output = {k: v for k, v in result.items() if k != "debug_snippet"}
        print(json.dumps(output, indent=2))
    else:
        if result["status"] in ("ok", "partial"):
            if result["percentage_used"] is not None:
                print(f"Usage: {result['percentage_used']}% used, {result['percentage_remaining']}% remaining")
            if result["reset_time"]:
                print(f"Next reset: {result['reset_time']}")
            if result["percentage_used"] is None and result["reset_time"]:
                print("(Could not find usage percentage, but found reset time.)")
        elif result["status"] == "not_found":
            print("Could not find usage percentage or reset time on the page.")
            if "debug_snippet" in result:
                print(f"Page preview:\n{result['debug_snippet']}")
        else:
            print(f"Error: {result.get('error', 'unknown')}")

    sys.exit(0 if result["status"] in ("ok", "partial") else 1)


if __name__ == "__main__":
    main()
