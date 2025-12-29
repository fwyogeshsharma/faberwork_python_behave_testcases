"""
Base Page Object for Faberwork Test Automation
Contains common methods and functionality shared across all pages
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from loguru import logger
from typing import List, Optional, Tuple
import time

from utils.config import Config
from utils.helpers import (
    wait_for_element,
    wait_for_element_to_be_clickable,
    wait_for_element_visibility,
    wait_for_elements,
    scroll_to_element,
    take_screenshot,
    is_element_present,
    is_element_visible,
)


class BasePage:
    """Base page class with common methods for all page objects"""

    def __init__(self, driver: WebDriver):
        """
        Initialize BasePage

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
        logger.debug(f"Initialized {self.__class__.__name__}")

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to(self, url: str):
        """
        Navigate to a specific URL

        Args:
            url: URL to navigate to
        """
        try:
            self.driver.get(url)
            logger.info(f"Navigated to: {url}")
            self.wait_for_page_load()
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise

    def get_current_url(self) -> str:
        """Get the current page URL"""
        url = self.driver.current_url
        logger.debug(f"Current URL: {url}")
        return url

    def get_page_title(self) -> str:
        """Get the current page title"""
        title = self.driver.title
        logger.debug(f"Page title: {title}")
        return title

    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        logger.info("Page refreshed")
        self.wait_for_page_load()

    def go_back(self):
        """Navigate back in browser history"""
        self.driver.back()
        logger.info("Navigated back")
        self.wait_for_page_load()

    def go_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()
        logger.info("Navigated forward")
        self.wait_for_page_load()

    # ============================================
    # Element Interaction Methods
    # ============================================

    def find_element(self, locator: Tuple[str, str]) -> Optional[WebElement]:
        """
        Find a single element

        Args:
            locator: Tuple of (By, value)

        Returns:
            WebElement or None
        """
        return wait_for_element(self.driver, locator)

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Find multiple elements

        Args:
            locator: Tuple of (By, value)

        Returns:
            List of WebElements
        """
        return wait_for_elements(self.driver, locator)

    def click(self, locator: Tuple[str, str], wait_clickable: bool = True):
        """
        Click on an element

        Args:
            locator: Tuple of (By, value)
            wait_clickable: Wait for element to be clickable
        """
        try:
            if wait_clickable:
                element = wait_for_element_to_be_clickable(self.driver, locator)
            else:
                element = self.find_element(locator)

            if element:
                scroll_to_element(self.driver, element)
                element.click()
                logger.info(f"Clicked element: {locator}")
            else:
                raise NoSuchElementException(f"Element not found: {locator}")

        except ElementClickInterceptedException:
            logger.warning(f"Element click intercepted for {locator}, trying JavaScript click")
            self.click_with_js(locator)

        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            take_screenshot(self.driver, f"click_failed_{locator[1]}")
            raise

    def click_with_js(self, locator: Tuple[str, str]):
        """
        Click element using JavaScript

        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.find_element(locator)
            if element:
                self.driver.execute_script("arguments[0].click();", element)
                logger.info(f"Clicked element with JS: {locator}")
        except Exception as e:
            logger.error(f"Failed to click with JS {locator}: {str(e)}")
            raise

    def double_click(self, locator: Tuple[str, str]):
        """
        Double click on an element

        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = wait_for_element_to_be_clickable(self.driver, locator)
            if element:
                self.actions.double_click(element).perform()
                logger.info(f"Double clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to double click {locator}: {str(e)}")
            raise

    def right_click(self, locator: Tuple[str, str]):
        """
        Right click (context click) on an element

        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = wait_for_element_to_be_clickable(self.driver, locator)
            if element:
                self.actions.context_click(element).perform()
                logger.info(f"Right clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to right click {locator}: {str(e)}")
            raise

    def hover(self, locator: Tuple[str, str]):
        """
        Hover over an element

        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = wait_for_element_visibility(self.driver, locator)
            if element:
                self.actions.move_to_element(element).perform()
                logger.info(f"Hovered over element: {locator}")
                time.sleep(0.5)  # Small delay for hover effects
        except Exception as e:
            logger.error(f"Failed to hover over {locator}: {str(e)}")
            raise

    def enter_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True):
        """
        Enter text into an input field

        Args:
            locator: Tuple of (By, value)
            text: Text to enter
            clear_first: Clear field before entering text
        """
        try:
            element = wait_for_element_visibility(self.driver, locator)
            if element:
                scroll_to_element(self.driver, element)

                if clear_first:
                    element.clear()

                element.send_keys(text)
                logger.info(f"Entered text into {locator}: '{text}'")
        except Exception as e:
            logger.error(f"Failed to enter text into {locator}: {str(e)}")
            take_screenshot(self.driver, f"enter_text_failed_{locator[1]}")
            raise

    def clear_text(self, locator: Tuple[str, str]):
        """
        Clear text from an input field

        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.find_element(locator)
            if element:
                element.clear()
                logger.info(f"Cleared text from: {locator}")
        except Exception as e:
            logger.error(f"Failed to clear text from {locator}: {str(e)}")
            raise

    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text from an element

        Args:
            locator: Tuple of (By, value)

        Returns:
            str: Element text
        """
        try:
            element = self.find_element(locator)
            if element:
                text = element.text
                logger.debug(f"Got text from {locator}: '{text}'")
                return text
            return ""
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {str(e)}")
            return ""

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get attribute value from an element

        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name

        Returns:
            str: Attribute value
        """
        try:
            element = self.find_element(locator)
            if element:
                value = element.get_attribute(attribute)
                logger.debug(f"Got attribute '{attribute}' from {locator}: '{value}'")
                return value or ""
            return ""
        except Exception as e:
            logger.error(f"Failed to get attribute from {locator}: {str(e)}")
            return ""

    def is_element_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is displayed

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if displayed, False otherwise
        """
        return is_element_visible(self.driver, locator)

    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is enabled

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            element = self.find_element(locator)
            return element.is_enabled() if element else False
        except:
            return False

    def is_element_selected(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is selected (for checkboxes/radio buttons)

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if selected, False otherwise
        """
        try:
            element = self.find_element(locator)
            return element.is_selected() if element else False
        except:
            return False

    # ============================================
    # Wait Methods
    # ============================================

    def wait_for_element_to_appear(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Wait for element to appear

        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time

        Returns:
            bool: True if element appeared, False otherwise
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            wait_for_element(self.driver, locator, timeout)
            logger.info(f"Element appeared: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element did not appear within {timeout}s: {locator}")
            return False

    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Wait for element to disappear

        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time

        Returns:
            bool: True if element disappeared, False otherwise
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.info(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element did not disappear within {timeout}s: {locator}")
            return False

    def wait_for_page_load(self, timeout: int = None):
        """
        Wait for page to fully load

        Args:
            timeout: Maximum wait time
        """
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logger.debug("Page loaded successfully")
        except TimeoutException:
            logger.warning(f"Page did not load within {timeout}s")

    # ============================================
    # Scroll Methods
    # ============================================

    def scroll_to_element_locator(self, locator: Tuple[str, str]):
        """
        Scroll to an element by locator

        Args:
            locator: Tuple of (By, value)
        """
        element = self.find_element(locator)
        if element:
            scroll_to_element(self.driver, element)

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.debug("Scrolled to top")
        time.sleep(0.3)

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("Scrolled to bottom")
        time.sleep(0.3)

    # ============================================
    # Screenshot Methods
    # ============================================

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take a screenshot

        Args:
            name: Name for screenshot file

        Returns:
            str: Path to screenshot
        """
        return take_screenshot(self.driver, name)

    # ============================================
    # JavaScript Methods
    # ============================================

    def execute_script(self, script: str, *args):
        """
        Execute JavaScript code

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Any: Result of script execution
        """
        try:
            result = self.driver.execute_script(script, *args)
            logger.debug(f"Executed JavaScript: {script[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Failed to execute JavaScript: {str(e)}")
            raise

    # ============================================
    # Validation Methods
    # ============================================

    def verify_url_contains(self, expected_text: str) -> bool:
        """
        Verify URL contains expected text

        Args:
            expected_text: Text expected in URL

        Returns:
            bool: True if URL contains text
        """
        current_url = self.get_current_url()
        result = expected_text in current_url
        if result:
            logger.info(f"✓ URL contains '{expected_text}'")
        else:
            logger.warning(f"✗ URL does not contain '{expected_text}'. Current URL: {current_url}")
        return result

    def verify_title_contains(self, expected_text: str) -> bool:
        """
        Verify page title contains expected text

        Args:
            expected_text: Text expected in title

        Returns:
            bool: True if title contains text
        """
        title = self.get_page_title()
        result = expected_text in title
        if result:
            logger.info(f"✓ Title contains '{expected_text}'")
        else:
            logger.warning(f"✗ Title does not contain '{expected_text}'. Current title: {title}")
        return result
