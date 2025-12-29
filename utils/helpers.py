"""
Helper utilities for Faberwork Test Automation
Common functions used across the test framework
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from loguru import logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .config import Config


def take_screenshot(driver: WebDriver, name: str = "screenshot") -> str:
    """
    Take a screenshot and save it to the screenshots directory

    Args:
        driver: WebDriver instance
        name: Name for the screenshot file

    Returns:
        str: Path to the saved screenshot
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = Config.SCREENSHOT_DIR / filename

        driver.save_screenshot(str(filepath))
        logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)

    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return ""


def wait_for_element(
    driver: WebDriver,
    locator: tuple,
    timeout: int = None,
    condition=EC.presence_of_element_located
) -> Optional[WebElement]:
    """
    Wait for an element to meet a specific condition

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
        condition: Expected condition to wait for

    Returns:
        WebElement or None
    """
    timeout = timeout or Config.EXPLICIT_WAIT

    try:
        element = WebDriverWait(driver, timeout).until(
            condition(locator)
        )
        logger.debug(f"Element found: {locator}")
        return element

    except TimeoutException:
        logger.warning(f"Element not found within {timeout}s: {locator}")
        return None


def wait_for_elements(
    driver: WebDriver,
    locator: tuple,
    timeout: int = None
) -> List[WebElement]:
    """
    Wait for multiple elements to be present

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds

    Returns:
        List of WebElements
    """
    timeout = timeout or Config.EXPLICIT_WAIT

    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        logger.debug(f"Found {len(elements)} elements: {locator}")
        return elements

    except TimeoutException:
        logger.warning(f"Elements not found within {timeout}s: {locator}")
        return []


def wait_for_element_to_be_clickable(
    driver: WebDriver,
    locator: tuple,
    timeout: int = None
) -> Optional[WebElement]:
    """
    Wait for an element to be clickable

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds

    Returns:
        WebElement or None
    """
    return wait_for_element(driver, locator, timeout, EC.element_to_be_clickable)


def wait_for_element_visibility(
    driver: WebDriver,
    locator: tuple,
    timeout: int = None
) -> Optional[WebElement]:
    """
    Wait for an element to be visible

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds

    Returns:
        WebElement or None
    """
    return wait_for_element(driver, locator, timeout, EC.visibility_of_element_located)


def is_element_present(driver: WebDriver, locator: tuple) -> bool:
    """
    Check if an element is present in the DOM

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)

    Returns:
        bool: True if element is present, False otherwise
    """
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False


def is_element_visible(driver: WebDriver, locator: tuple) -> bool:
    """
    Check if an element is visible

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)

    Returns:
        bool: True if element is visible, False otherwise
    """
    try:
        element = driver.find_element(*locator)
        return element.is_displayed()
    except NoSuchElementException:
        return False


def scroll_to_element(driver: WebDriver, element: WebElement):
    """
    Scroll to bring an element into view

    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)  # Small delay for smooth scrolling
        logger.debug("Scrolled to element")
    except Exception as e:
        logger.error(f"Failed to scroll to element: {str(e)}")


def scroll_to_top(driver: WebDriver):
    """
    Scroll to the top of the page

    Args:
        driver: WebDriver instance
    """
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)
        logger.debug("Scrolled to top of page")
    except Exception as e:
        logger.error(f"Failed to scroll to top: {str(e)}")


def scroll_to_bottom(driver: WebDriver):
    """
    Scroll to the bottom of the page

    Args:
        driver: WebDriver instance
    """
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        logger.debug("Scrolled to bottom of page")
    except Exception as e:
        logger.error(f"Failed to scroll to bottom: {str(e)}")


def highlight_element(driver: WebDriver, element: WebElement, duration: float = 0.5):
    """
    Highlight an element (useful for debugging)

    Args:
        driver: WebDriver instance
        element: WebElement to highlight
        duration: How long to highlight in seconds
    """
    try:
        original_style = element.get_attribute('style')
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 3px solid red; background-color: yellow;"
        )
        time.sleep(duration)
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style
        )
    except Exception as e:
        logger.error(f"Failed to highlight element: {str(e)}")


def get_current_url(driver: WebDriver) -> str:
    """
    Get the current URL

    Args:
        driver: WebDriver instance

    Returns:
        str: Current URL
    """
    try:
        url = driver.current_url
        logger.debug(f"Current URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Failed to get current URL: {str(e)}")
        return ""


def get_page_title(driver: WebDriver) -> str:
    """
    Get the page title

    Args:
        driver: WebDriver instance

    Returns:
        str: Page title
    """
    try:
        title = driver.title
        logger.debug(f"Page title: {title}")
        return title
    except Exception as e:
        logger.error(f"Failed to get page title: {str(e)}")
        return ""


def switch_to_frame(driver: WebDriver, frame_locator: tuple):
    """
    Switch to an iframe

    Args:
        driver: WebDriver instance
        frame_locator: Tuple of (By, value) for the frame
    """
    try:
        frame = wait_for_element(driver, frame_locator)
        driver.switch_to.frame(frame)
        logger.debug(f"Switched to frame: {frame_locator}")
    except Exception as e:
        logger.error(f"Failed to switch to frame: {str(e)}")


def switch_to_default_content(driver: WebDriver):
    """
    Switch back to default content (out of iframe)

    Args:
        driver: WebDriver instance
    """
    try:
        driver.switch_to.default_content()
        logger.debug("Switched to default content")
    except Exception as e:
        logger.error(f"Failed to switch to default content: {str(e)}")


def switch_to_window(driver: WebDriver, window_index: int = -1):
    """
    Switch to a different browser window

    Args:
        driver: WebDriver instance
        window_index: Index of the window to switch to (-1 for last window)
    """
    try:
        windows = driver.window_handles
        if window_index == -1:
            driver.switch_to.window(windows[-1])
        else:
            driver.switch_to.window(windows[window_index])
        logger.debug(f"Switched to window index: {window_index}")
    except Exception as e:
        logger.error(f"Failed to switch to window: {str(e)}")


def close_current_window(driver: WebDriver):
    """
    Close the current browser window

    Args:
        driver: WebDriver instance
    """
    try:
        driver.close()
        logger.debug("Closed current window")
    except Exception as e:
        logger.error(f"Failed to close window: {str(e)}")


def accept_alert(driver: WebDriver) -> bool:
    """
    Accept a JavaScript alert

    Args:
        driver: WebDriver instance

    Returns:
        bool: True if alert was accepted, False otherwise
    """
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
        logger.debug("Alert accepted")
        return True
    except TimeoutException:
        logger.debug("No alert present")
        return False


def dismiss_alert(driver: WebDriver) -> bool:
    """
    Dismiss a JavaScript alert

    Args:
        driver: WebDriver instance

    Returns:
        bool: True if alert was dismissed, False otherwise
    """
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.dismiss()
        logger.debug("Alert dismissed")
        return True
    except TimeoutException:
        logger.debug("No alert present")
        return False


def get_alert_text(driver: WebDriver) -> str:
    """
    Get text from a JavaScript alert

    Args:
        driver: WebDriver instance

    Returns:
        str: Alert text or empty string
    """
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        text = alert.text
        logger.debug(f"Alert text: {text}")
        return text
    except TimeoutException:
        logger.debug("No alert present")
        return ""


def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Load data from a JSON file

    Args:
        filepath: Path to JSON file

    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.debug(f"Loaded JSON file: {filepath}")
        return data
    except Exception as e:
        logger.error(f"Failed to load JSON file: {str(e)}")
        return {}


def save_json_file(data: Dict[str, Any], filepath: str):
    """
    Save data to a JSON file

    Args:
        data: Data to save
        filepath: Path to save the file
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.debug(f"Saved JSON file: {filepath}")
    except Exception as e:
        logger.error(f"Failed to save JSON file: {str(e)}")


def generate_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    Generate a timestamp string

    Args:
        format_str: strftime format string

    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime(format_str)


def wait_for_page_load(driver: WebDriver, timeout: int = None):
    """
    Wait for page to fully load

    Args:
        driver: WebDriver instance
        timeout: Maximum wait time in seconds
    """
    timeout = timeout or Config.PAGE_LOAD_TIMEOUT

    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        logger.debug("Page loaded successfully")
    except TimeoutException:
        logger.warning(f"Page did not load within {timeout}s")
