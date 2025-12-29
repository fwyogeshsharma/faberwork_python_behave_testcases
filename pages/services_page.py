"""
Services Page Object for Faberwork Test Automation
www.faberwork.com/services page elements and interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from .base_page import BasePage
from utils.config import Config


class ServicesPage(BasePage):
    """Page Object for Faberwork Services page"""

    # ============================================
    # Locators
    # ============================================

    # Page Header
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Services to Drive Your Business Forward') or contains(text(), 'Services')]")
    PAGE_SUBTITLE = (By.CSS_SELECTOR, "p")

    # Individual Services (8 services)
    SNOWPRO_SECTION = (By.XPATH, "//*[contains(text(), 'SnowPro® Certified Developers')]")
    AI_IMPLEMENTATION_SECTION = (By.XPATH, "//*[contains(text(), 'Cost Effective AI Implementation')]")
    MOBILE_APP_SECTION = (By.XPATH, "//*[contains(text(), 'Mobile App Development')]")
    SOFTWARE_DEV_SECTION = (By.XPATH, "//*[contains(text(), 'Software Development')]")
    ERP_SOLUTIONS_SECTION = (By.XPATH, "//*[contains(text(), 'ERP Solutions')]")
    DATABASE_SECTION = (By.XPATH, "//*[contains(text(), 'Database Solutions')]")
    SOFTWARE_REENGINEERING_SECTION = (By.XPATH, "//*[contains(text(), 'Software Re-engineering')]")
    TEST_AUTOMATION_SECTION = (By.XPATH, "//*[contains(text(), 'Test Automation')]")

    # Sections
    TRUSTED_COMPANIES_SECTION = (By.XPATH, "//*[contains(text(), 'Trusted by Leading Technology Companies')]")
    WHAT_SETS_APART_SECTION = (By.XPATH, "//*[contains(text(), 'What Sets Us Apart')]")
    LETS_WORK_TOGETHER_SECTION = (By.XPATH, "//*[contains(text(), \"Let's Work Together\")]")

    # CTA Buttons
    START_NOW_BUTTON = (By.XPATH, "//a[contains(text(), 'START NOW') or @href='mailto:info@faberwork.com']")
    GET_STARTED_BUTTON = (By.XPATH, "//a[contains(text(), 'Get Started')]")
    FREE_CONSULTATION_LINK = (By.XPATH, "//a[contains(text(), 'Get a Free Consultation')]")

    # Contact Info
    PHONE_USA = (By.XPATH, "//a[contains(text(), '+1-410-884-9169')]")
    PHONE_INDIA = (By.XPATH, "//a[contains(text(), '+91-74140-82984')]")

    # Service Details
    SERVICE_DESCRIPTIONS = (By.CSS_SELECTOR, ".service-description, .description")
    SERVICE_FEATURES = (By.CSS_SELECTOR, ".service-features, .features li")

    def __init__(self, driver: WebDriver):
        """Initialize ServicesPage"""
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/services"
        logger.debug("ServicesPage initialized")

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to_services_page(self):
        """Navigate to the services page"""
        self.navigate_to(self.url)
        logger.info(f"Navigated to services page: {self.url}")

    # ============================================
    # Service Interaction Methods
    # ============================================

    def get_page_title(self) -> str:
        """Get the services page title"""
        return self.get_text(self.PAGE_TITLE)

    def get_services_count(self) -> int:
        """Get the number of services displayed"""
        services = self.find_elements(self.SERVICE_CARDS)
        count = len(services)
        logger.info(f"Found {count} services")
        return count

    def click_service_by_name(self, service_name: str):
        """
        Click on a specific service by name

        Args:
            service_name: Name of the service
        """
        locator = (By.XPATH, f"//*[contains(text(), '{service_name}')]")
        self.scroll_to_element_locator(locator)
        self.click(locator)
        logger.info(f"Clicked service: {service_name}")

    def click_learn_more(self, index: int = 0):
        """
        Click 'Learn More' button

        Args:
            index: Index of the button (default 0 for first)
        """
        buttons = self.find_elements(self.LEARN_MORE_BUTTONS)
        if buttons and len(buttons) > index:
            buttons[index].click()
            logger.info(f"Clicked Learn More button at index {index}")

    def is_service_displayed(self, service_name: str) -> bool:
        """
        Check if a specific service is displayed

        Args:
            service_name: Name of the service to check

        Returns:
            bool: True if service is displayed
        """
        locator = (By.XPATH, f"//*[contains(text(), '{service_name}')]")
        return self.is_element_displayed(locator)

    # ============================================
    # Validation Methods
    # ============================================

    def verify_services_page_loaded(self) -> bool:
        """Verify that services page is loaded successfully"""
        checks = [
            self.is_element_displayed(self.PAGE_TITLE),
            self.is_element_displayed(self.SERVICES_LIST) or self.get_services_count() > 0,
        ]
        result = any(checks)

        if result:
            logger.info("✓ Services page loaded successfully")
        else:
            logger.warning("✗ Services page did not load properly")
            self.take_screenshot("services_page_load_failed")

        return result
