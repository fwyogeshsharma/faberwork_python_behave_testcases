"""
Contact Page Object for Faberwork Test Automation
www.faberwork.com/contact page elements and interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from .base_page import BasePage
from utils.config import Config


class ContactPage(BasePage):
    """Page Object for Faberwork Contact page"""

    # ============================================
    # Locators
    # ============================================

    # Page Header
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title")
    PAGE_DESCRIPTION = (By.CSS_SELECTOR, ".description, .page-description")

    # Contact Form (Modal)
    CONTACT_FORM = (By.ID, "consultationForm")
    OPEN_MODAL_BUTTON = (By.CSS_SELECTOR, ".openModalButton")
    FORM_NAME = (By.CSS_SELECTOR, ".input_name")
    FORM_EMAIL = (By.CSS_SELECTOR, ".input_email")
    FORM_PHONE = (By.CSS_SELECTOR, ".input_phone")
    FORM_COMPANY = (By.CSS_SELECTOR, ".input_company")
    FORM_MESSAGE = (By.CSS_SELECTOR, "textarea[name='message']")
    FORM_SUBMIT = (By.CSS_SELECTOR, "#consultationForm button[type='submit']")

    # Form Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".toast.text-bg-success, #alert-container .toast")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".toast.text-bg-warning, .toast.text-bg-danger")
    VALIDATION_ERRORS = (By.CSS_SELECTOR, ".invalid-feedback, .error")

    # Contact Information
    CONTACT_INFO_SECTION = (By.CSS_SELECTOR, "footer")
    EMAIL_ADDRESS = (By.CSS_SELECTOR, "a[href='mailto:info@faberwork.com']")

    # Social Media Links
    LINKEDIN_LINK = (By.CSS_SELECTOR, "a[href='https://in.linkedin.com/company/faberwork-llc']")

    # Map
    MAP_SECTION = (By.CSS_SELECTOR, ".map, #map, iframe[src*='maps']")

    def __init__(self, driver: WebDriver):
        """Initialize ContactPage"""
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/contact"
        logger.debug("ContactPage initialized")

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to_contact_page(self):
        """Navigate to the contact page"""
        self.navigate_to(self.url)
        logger.info(f"Navigated to contact page: {self.url}")

    # ============================================
    # Form Interaction Methods
    # ============================================

    def fill_contact_form(self, name: str, email: str, phone: str = "",
                         company: str = "", subject: str = "", message: str = ""):
        """
        Fill in the contact form

        Args:
            name: Full name
            email: Email address
            phone: Phone number (optional)
            company: Company name (optional)
            subject: Subject (optional)
            message: Message text
        """
        logger.info("Filling contact form")

        self.enter_text(self.FORM_NAME, name)
        self.enter_text(self.FORM_EMAIL, email)

        if phone:
            self.enter_text(self.FORM_PHONE, phone)

        if company and self.is_element_displayed(self.FORM_COMPANY):
            self.enter_text(self.FORM_COMPANY, company)

        if subject and self.is_element_displayed(self.FORM_SUBJECT):
            self.enter_text(self.FORM_SUBJECT, subject)

        if message:
            self.enter_text(self.FORM_MESSAGE, message)

        logger.info("Contact form filled")

    def submit_contact_form(self):
        """Submit the contact form"""
        self.click(self.FORM_SUBMIT)
        logger.info("Submitted contact form")

    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed"""
        return self.wait_for_element_to_appear(self.SUCCESS_MESSAGE, timeout=5)

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.wait_for_element_to_appear(self.ERROR_MESSAGE, timeout=3)

    def get_success_message_text(self) -> str:
        """Get the success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_error_message_text(self) -> str:
        """Get the error message text"""
        return self.get_text(self.ERROR_MESSAGE)

    def get_validation_errors(self) -> list:
        """Get all validation error messages"""
        error_elements = self.find_elements(self.VALIDATION_ERRORS)
        errors = [elem.text for elem in error_elements if elem.text]
        logger.info(f"Found {len(errors)} validation errors")
        return errors

    # ============================================
    # Contact Information Methods
    # ============================================

    def get_contact_phone(self) -> str:
        """Get the displayed contact phone number"""
        return self.get_text(self.PHONE_NUMBER)

    def get_contact_email(self) -> str:
        """Get the displayed contact email"""
        return self.get_text(self.EMAIL_ADDRESS)

    def get_contact_address(self) -> str:
        """Get the displayed contact address"""
        return self.get_text(self.ADDRESS)

    # ============================================
    # Social Media Methods
    # ============================================

    def click_linkedin_link(self):
        """Click on LinkedIn social media link"""
        if self.is_element_displayed(self.LINKEDIN_LINK):
            self.click(self.LINKEDIN_LINK)
            logger.info("Clicked LinkedIn link")

    def is_map_displayed(self) -> bool:
        """Check if map is displayed"""
        return self.is_element_displayed(self.MAP_SECTION)

    # ============================================
    # Validation Methods
    # ============================================

    def verify_contact_page_loaded(self) -> bool:
        """Verify that contact page is loaded successfully"""
        checks = [
            self.is_element_displayed(self.PAGE_TITLE),
            self.is_element_displayed(self.CONTACT_FORM),
        ]
        result = any(checks)

        if result:
            logger.info("✓ Contact page loaded successfully")
        else:
            logger.warning("✗ Contact page did not load properly")
            self.take_screenshot("contact_page_load_failed")

        return result

    def verify_all_form_fields_present(self) -> bool:
        """Verify all required form fields are present"""
        required_fields = [
            self.FORM_NAME,
            self.FORM_EMAIL,
            self.FORM_MESSAGE,
            self.FORM_SUBMIT,
        ]

        results = [self.is_element_displayed(field) for field in required_fields]
        all_present = all(results)

        if all_present:
            logger.info("✓ All required form fields are present")
        else:
            logger.warning("✗ Some required form fields are missing")

        return all_present
