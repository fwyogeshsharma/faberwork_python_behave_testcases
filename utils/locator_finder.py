"""
Locator Finder Utility for Faberwork Test Automation
Helper tool to find and validate element locators
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from typing import List, Tuple, Optional
from loguru import logger


class LocatorFinder:
    """Utility class for finding and validating element locators"""

    def __init__(self, driver: WebDriver):
        """
        Initialize LocatorFinder

        Args:
            driver: WebDriver instance
        """
        self.driver = driver

    def find_by_text(self, text: str, exact: bool = False) -> List:
        """
        Find elements containing specific text

        Args:
            text: Text to search for
            exact: If True, match exact text; if False, match partial text

        Returns:
            list: List of matching WebElements
        """
        try:
            if exact:
                xpath = f"//*[text()='{text}']"
            else:
                xpath = f"//*[contains(text(), '{text}')]"

            elements = self.driver.find_elements(By.XPATH, xpath)
            logger.info(f"Found {len(elements)} elements with text: '{text}'")
            return elements

        except Exception as e:
            logger.error(f"Error finding elements by text: {str(e)}")
            return []

    def validate_locator(self, locator: Tuple[str, str]) -> bool:
        """
        Test if a locator can find an element

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if element found, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            logger.info(f"✓ Valid locator: {locator}")
            return True

        except NoSuchElementException:
            logger.warning(f"✗ Invalid locator: {locator}")
            return False

    def find_by_attribute(self, attribute: str, value: str) -> List:
        """
        Find elements by attribute value

        Args:
            attribute: Attribute name (e.g., 'class', 'id', 'data-testid')
            value: Attribute value

        Returns:
            list: List of matching WebElements
        """
        try:
            xpath = f"//*[@{attribute}='{value}']"
            elements = self.driver.find_elements(By.XPATH, xpath)
            logger.info(f"Found {len(elements)} elements with {attribute}='{value}'")
            return elements

        except Exception as e:
            logger.error(f"Error finding elements by attribute: {str(e)}")
            return []

    def find_all_links(self) -> List:
        """
        Find all links on the page

        Returns:
            list: List of all anchor elements
        """
        try:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            logger.info(f"Found {len(links)} links on the page")
            return links

        except Exception as e:
            logger.error(f"Error finding links: {str(e)}")
            return []

    def find_all_buttons(self) -> List:
        """
        Find all buttons on the page

        Returns:
            list: List of all button elements
        """
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit']")
            all_buttons = buttons + inputs
            logger.info(f"Found {len(all_buttons)} buttons on the page")
            return all_buttons

        except Exception as e:
            logger.error(f"Error finding buttons: {str(e)}")
            return []

    def find_all_inputs(self) -> List:
        """
        Find all input fields on the page

        Returns:
            list: List of all input elements
        """
        try:
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"Found {len(inputs)} input fields on the page")
            return inputs

        except Exception as e:
            logger.error(f"Error finding inputs: {str(e)}")
            return []

    def print_element_info(self, element):
        """
        Print detailed information about an element (for debugging)

        Args:
            element: WebElement to inspect
        """
        try:
            print("\n" + "="*60)
            print("ELEMENT INFORMATION")
            print("="*60)
            print(f"Tag Name: {element.tag_name}")
            print(f"Text: {element.text}")
            print(f"ID: {element.get_attribute('id')}")
            print(f"Class: {element.get_attribute('class')}")
            print(f"Name: {element.get_attribute('name')}")
            print(f"Type: {element.get_attribute('type')}")
            print(f"Value: {element.get_attribute('value')}")
            print(f"Href: {element.get_attribute('href')}")
            print(f"Data-testid: {element.get_attribute('data-testid')}")
            print(f"Displayed: {element.is_displayed()}")
            print(f"Enabled: {element.is_enabled()}")
            print(f"Location: {element.location}")
            print(f"Size: {element.size}")
            print("="*60 + "\n")

        except Exception as e:
            logger.error(f"Error printing element info: {str(e)}")

    def suggest_locators(self, element) -> dict:
        """
        Suggest multiple locator strategies for an element

        Args:
            element: WebElement to analyze

        Returns:
            dict: Dictionary of locator strategies
        """
        suggestions = {}

        try:
            # ID
            element_id = element.get_attribute('id')
            if element_id:
                suggestions['ID'] = (By.ID, element_id)

            # Name
            element_name = element.get_attribute('name')
            if element_name:
                suggestions['NAME'] = (By.NAME, element_name)

            # Class
            element_class = element.get_attribute('class')
            if element_class:
                suggestions['CSS_CLASS'] = (By.CSS_SELECTOR, f".{element_class.split()[0]}")

            # Data-testid
            testid = element.get_attribute('data-testid')
            if testid:
                suggestions['DATA_TESTID'] = (By.CSS_SELECTOR, f"[data-testid='{testid}']")

            # Tag + Text
            if element.text:
                suggestions['XPATH_TEXT'] = (By.XPATH, f"//{element.tag_name}[contains(text(), '{element.text[:20]}')]")

            # Link Text
            if element.tag_name == 'a' and element.text:
                suggestions['LINK_TEXT'] = (By.LINK_TEXT, element.text)

            logger.info(f"Generated {len(suggestions)} locator suggestions")
            return suggestions

        except Exception as e:
            logger.error(f"Error suggesting locators: {str(e)}")
            return {}

    def test_all_locator_strategies(self, element) -> dict:
        """
        Test all possible locator strategies for an element

        Args:
            element: WebElement to test

        Returns:
            dict: Results of each strategy
        """
        results = {}
        suggestions = self.suggest_locators(element)

        for strategy_name, locator in suggestions.items():
            is_valid = self.validate_locator(locator)
            results[strategy_name] = {
                'locator': locator,
                'valid': is_valid
            }

        return results
