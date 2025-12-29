"""
Home Page Object for Faberwork Test Automation
www.faberwork.com homepage elements and interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from .base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    """Page Object for Faberwork homepage"""

    # ============================================
    # Locators
    # ============================================

    # Header/Navigation
    LOGO = (By.CSS_SELECTOR, "img[src='/static/img/faberwork-logo-white.svg']")
    NAV_HOME = (By.CSS_SELECTOR, "a[href='/']")
    NAV_SERVICES = (By.CSS_SELECTOR, "a[href='/services']")
    NAV_INDUSTRIES = (By.CSS_SELECTOR, "a[href='/industries']")
    NAV_SUCCESS_STORIES = (By.CSS_SELECTOR, "a[href='/success-stories']")
    NAV_LATEST_THINKING = (By.CSS_SELECTOR, "a[href='/latest-thinking']")
    NAV_ABOUT = (By.CSS_SELECTOR, "a[href='/about-us']")
    NAV_CONTACT = (By.CSS_SELECTOR, "a[href='/contact-us']")

    # Hero Section
    HERO_SECTION = (By.CSS_SELECTOR, ".hero-section")
    HERO_TITLE = (By.XPATH, "//h1[contains(text(), 'Agentic AI')]")
    HERO_CTA_BUTTON = (By.CSS_SELECTOR, "a[href='/services']")

    # Services Section
    SERVICES_SECTION = (By.CSS_SELECTOR, ".services-section, #services")
    SERVICE_CARDS = (By.CSS_SELECTOR, ".service-card, .services .card")
    SNOWPRO_SERVICE = (By.XPATH, "//*[contains(text(), 'SnowPro')]")
    SOFTWARE_DEV_SERVICE = (By.XPATH, "//*[contains(text(), 'Software Development')]")
    MOBILE_APP_SERVICE = (By.XPATH, "//*[contains(text(), 'Mobile App')]")
    AI_SOLUTIONS_SERVICE = (By.XPATH, "//*[contains(text(), 'AI')]")
    DATABASE_SERVICE = (By.XPATH, "//*[contains(text(), 'Database')]")
    TEST_AUTOMATION_SERVICE = (By.XPATH, "//*[contains(text(), 'Test Automation')]")

    # Success Stories Carousel
    SUCCESS_STORIES_SECTION = (By.ID, "success-wrapper")
    CAROUSEL = (By.ID, "success-wrapper")
    CAROUSEL_NEXT = (By.ID, "next-arrow")
    CAROUSEL_PREV = (By.ID, "prev-arrow")
    CAROUSEL_ITEMS = (By.CSS_SELECTOR, ".success-content")
    CAROUSEL_DOTS = (By.ID, "success-dots")

    # Testimonials
    TESTIMONIAL_SECTION = (By.CSS_SELECTOR, ".testimonials")
    TESTIMONIAL_DOTS = (By.ID, "testimonial-dots")
    TESTIMONIAL_PREV = (By.ID, "prev-testimonial")
    TESTIMONIAL_NEXT = (By.ID, "next-testimonial")

    # Company Stats
    STATS_SECTION = (By.CSS_SELECTOR, ".stats, .company-stats, .achievements")
    STATS_YEARS = (By.XPATH, "//*[contains(text(), '20+ years') or contains(text(), '20 years')]")
    STATS_ENGINEERS = (By.XPATH, "//*[contains(text(), '50 engineers') or contains(text(), 'engineers')]")
    STATS_HOURS = (By.XPATH, "//*[contains(text(), '2M+') or contains(text(), 'hours')]")

    # Consultation Form
    CONSULTATION_FORM = (By.ID, "consultation-form")
    FORM_NAME = (By.CSS_SELECTOR, "input[name='consult-name']")
    FORM_COMPANY = (By.CSS_SELECTOR, "input[name='consult-company']")
    FORM_EMAIL = (By.CSS_SELECTOR, "input[name='consult-email']")
    FORM_PHONE = (By.CSS_SELECTOR, "input[name='consult-phone']")
    FORM_MESSAGE = (By.CSS_SELECTOR, "textarea[name='consult-message']")
    FORM_SUBMIT = (By.CSS_SELECTOR, "#consultation-form button[type='submit']")

    # Form Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".toast.text-bg-success, #alert-container .toast")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".toast.text-bg-warning, .toast.text-bg-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback, .error")

    # Newsletter
    NEWSLETTER_SECTION = (By.ID, "newsletter-form")
    NEWSLETTER_EMAIL = (By.CSS_SELECTOR, "input[name='letter-email']")
    NEWSLETTER_SUBMIT = (By.CSS_SELECTOR, "#newsletter-form button[type='submit']")

    # Footer
    FOOTER = (By.CSS_SELECTOR, "footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a")
    FOOTER_EMAIL = (By.CSS_SELECTOR, "a[href='mailto:info@faberwork.com']")
    FOOTER_LINKEDIN = (By.CSS_SELECTOR, "a[href='https://in.linkedin.com/company/faberwork-llc']")
    FOOTER_LOGO = (By.CSS_SELECTOR, "footer img[src='/static/img/faberwork-logo-white.svg']")

    # Chatbot
    CHATBOT_WIDGET = (By.ID, "chatbotDialog")
    CHATBOT_OPEN_BUTTON = (By.ID, "openChatbot")
    CHATBOT_CLOSE_BUTTON = (By.ID, "close-chat")
    CHATBOT_INPUT = (By.ID, "user-input")
    CHATBOT_SEND = (By.CSS_SELECTOR, "#chat-form button[type='submit']")
    CHATBOT_HISTORY = (By.ID, "chat-history")

    # Search
    SEARCH_INPUT = (By.ID, "articleSearch")
    SEARCH_BUTTON = (By.ID, "searchButton")
    SEARCH_RESULTS = (By.ID, "searchResults")
    SEARCH_RESULT_ITEMS = (By.CSS_SELECTOR, "#searchResults .dropdown-item")

    def __init__(self, driver: WebDriver):
        """Initialize HomePage"""
        super().__init__(driver)
        self.url = Config.BASE_URL
        logger.debug("HomePage initialized")

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to_homepage(self):
        """Navigate to the homepage"""
        self.navigate_to(self.url)
        logger.info(f"Navigated to homepage: {self.url}")

    def click_logo(self):
        """Click on the logo (usually returns to homepage)"""
        self.click(self.LOGO)
        logger.info("Clicked on logo")

    def click_services_menu(self):
        """Click on Services navigation menu"""
        self.click(self.NAV_SERVICES)
        logger.info("Clicked Services menu")

    def click_industries_menu(self):
        """Click on Industries navigation menu"""
        self.click(self.NAV_INDUSTRIES)
        logger.info("Clicked Industries menu")

    def click_success_stories_menu(self):
        """Click on Success Stories navigation menu"""
        self.click(self.NAV_SUCCESS_STORIES)
        logger.info("Clicked Success Stories menu")

    def click_latest_thinking_menu(self):
        """Click on Latest Thinking navigation menu"""
        self.click(self.NAV_LATEST_THINKING)
        logger.info("Clicked Latest Thinking menu")

    def click_about_menu(self):
        """Click on About Us navigation menu"""
        self.click(self.NAV_ABOUT)
        logger.info("Clicked About Us menu")

    def click_contact_menu(self):
        """Click on Contact Us navigation menu"""
        self.click(self.NAV_CONTACT)
        logger.info("Clicked Contact Us menu")

    # ============================================
    # Hero Section Methods
    # ============================================

    def click_hero_cta_button(self):
        """Click the CTA button in hero section"""
        self.click(self.HERO_CTA_BUTTON)
        logger.info("Clicked hero CTA button")

    def get_hero_title(self) -> str:
        """Get the hero section title text"""
        return self.get_text(self.HERO_TITLE)

    # ============================================
    # Services Section Methods
    # ============================================

    def is_services_section_displayed(self) -> bool:
        """Check if services section is visible"""
        return self.is_element_displayed(self.SERVICES_SECTION)

    def get_service_cards_count(self) -> int:
        """Get the number of service cards displayed"""
        cards = self.find_elements(self.SERVICE_CARDS)
        count = len(cards)
        logger.info(f"Found {count} service cards")
        return count

    def click_service_by_name(self, service_name: str):
        """
        Click on a specific service by name

        Args:
            service_name: Name of the service to click
        """
        locator = (By.XPATH, f"//*[contains(text(), '{service_name}')]")
        self.click(locator)
        logger.info(f"Clicked service: {service_name}")

    # ============================================
    # Carousel Methods
    # ============================================

    def click_carousel_next(self):
        """Click next button on carousel"""
        self.click(self.CAROUSEL_NEXT)
        logger.info("Clicked carousel next")

    def click_carousel_prev(self):
        """Click previous button on carousel"""
        self.click(self.CAROUSEL_PREV)
        logger.info("Clicked carousel prev")

    def get_carousel_items_count(self) -> int:
        """Get the number of carousel items"""
        items = self.find_elements(self.CAROUSEL_ITEMS)
        count = len(items)
        logger.info(f"Found {count} carousel items")
        return count

    # ============================================
    # Consultation Form Methods
    # ============================================

    def fill_consultation_form(self, name: str, company: str, email: str, phone: str, message: str = ""):
        """
        Fill in the consultation form

        Args:
            name: Full name
            company: Company name
            email: Email address
            phone: Phone number
            message: Message (optional)
        """
        logger.info("Filling consultation form")

        self.enter_text(self.FORM_NAME, name)
        self.enter_text(self.FORM_COMPANY, company)
        self.enter_text(self.FORM_EMAIL, email)
        self.enter_text(self.FORM_PHONE, phone)

        if message and self.is_element_displayed(self.FORM_MESSAGE):
            self.enter_text(self.FORM_MESSAGE, message)

        logger.info("Consultation form filled")

    def submit_consultation_form(self):
        """Submit the consultation form"""
        self.click(self.FORM_SUBMIT)
        logger.info("Submitted consultation form")

    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed"""
        return self.wait_for_element_to_appear(self.SUCCESS_MESSAGE, timeout=5)

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_displayed(self.ERROR_MESSAGE)

    def get_success_message_text(self) -> str:
        """Get the success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_error_message_text(self) -> str:
        """Get the error message text"""
        return self.get_text(self.ERROR_MESSAGE)

    # ============================================
    # Newsletter Methods
    # ============================================

    def subscribe_to_newsletter(self, email: str):
        """
        Subscribe to newsletter

        Args:
            email: Email address for subscription
        """
        logger.info(f"Subscribing to newsletter with: {email}")
        self.scroll_to_element_locator(self.NEWSLETTER_SECTION)
        self.enter_text(self.NEWSLETTER_EMAIL, email)
        self.click(self.NEWSLETTER_SUBMIT)
        logger.info("Newsletter subscription submitted")

    # ============================================
    # Chatbot Methods
    # ============================================

    def open_chatbot(self):
        """Open the chatbot widget"""
        if self.is_element_displayed(self.CHATBOT_OPEN_BUTTON):
            self.click(self.CHATBOT_OPEN_BUTTON)
            logger.info("Opened chatbot")

    def send_chatbot_message(self, message: str):
        """
        Send a message in chatbot

        Args:
            message: Message to send
        """
        self.enter_text(self.CHATBOT_INPUT, message)
        self.click(self.CHATBOT_SEND)
        logger.info(f"Sent chatbot message: {message}")

    # ============================================
    # Search Methods
    # ============================================

    def search_for(self, query: str):
        """
        Perform a search

        Args:
            query: Search query
        """
        self.enter_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        logger.info(f"Searched for: {query}")

    # ============================================
    # Validation Methods
    # ============================================

    def verify_homepage_loaded(self) -> bool:
        """Verify that homepage is loaded successfully"""
        checks = [
            self.is_element_displayed(self.LOGO),
            self.is_element_displayed(self.NAV_SERVICES),
        ]
        result = all(checks)

        if result:
            logger.info("✓ Homepage loaded successfully")
        else:
            logger.warning("✗ Homepage did not load properly")
            self.take_screenshot("homepage_load_failed")

        return result

    def verify_all_navigation_links_present(self) -> bool:
        """Verify all main navigation links are present"""
        nav_links = [
            self.NAV_SERVICES,
            self.NAV_INDUSTRIES,
            self.NAV_SUCCESS_STORIES,
            self.NAV_LATEST_THINKING,
            self.NAV_ABOUT,
            self.NAV_CONTACT,
        ]

        results = [self.is_element_displayed(link) for link in nav_links]
        all_present = all(results)

        if all_present:
            logger.info("✓ All navigation links are present")
        else:
            logger.warning("✗ Some navigation links are missing")

        return all_present
