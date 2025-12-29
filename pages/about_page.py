"""
About Page Object for Faberwork Test Automation
www.faberwork.com/about page elements and interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from .base_page import BasePage
from utils.config import Config


class AboutPage(BasePage):
    """Page Object for Faberwork About Us page"""

    # ============================================
    # Locators
    # ============================================

    # Page Header
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Who We Are')]")
    ESTABLISHED_TEXT = (By.XPATH, "//*[contains(text(), 'Established 2003')]")
    PAGE_DESCRIPTION = (By.CSS_SELECTOR, "p")

    # Company Information
    COMPANY_OVERVIEW = (By.XPATH, "//*[contains(text(), 'software solutions and services company')]")
    SNOWFLAKE_PARTNER = (By.XPATH, "//*[contains(text(), 'Snowflake Partner Network')]")
    MISSION_SECTION = (By.XPATH, "//*[contains(text(), 'enterprise application consulting')]")
    VISION_SECTION = (By.CSS_SELECTOR, "p")
    VALUES_SECTION = (By.CSS_SELECTOR, "p")

    # Leadership Team
    TEAM_SECTION = (By.CSS_SELECTOR, "div")
    ALOK_PANCHOLI = (By.XPATH, "//*[contains(text(), 'Alok Pancholi')]")
    YOGESH_SHARMA = (By.XPATH, "//*[contains(text(), 'Yogesh Sharma')]")
    JAIDEEP_SINGH = (By.XPATH, "//*[contains(text(), 'Jaideep Singh')]")
    RAM_SINGH = (By.XPATH, "//*[contains(text(), 'Ram Singh') and contains(text(), 'Senior Technical Lead')]")
    SAURABH_JAIN = (By.XPATH, "//*[contains(text(), 'Saurabh Jain')]")
    VIKAS_SHARMA = (By.XPATH, "//*[contains(text(), 'Vikas Sharma')]")

    # Team Photos
    ALOK_PHOTO = (By.CSS_SELECTOR, "img[src*='alok-pancholi']")
    YOGESH_PHOTO = (By.CSS_SELECTOR, "img[src*='yogesh-sharma']")

    # Read More Toggle
    READ_MORE_BUTTONS = (By.CSS_SELECTOR, ".employee_read_more, button[onclick*='toggleReadMore']")
    TEAM_MEMBER_NAMES = (By.XPATH, "//h3 | //h4")
    TEAM_MEMBER_TITLES = (By.XPATH, "//*[contains(text(), 'CEO') or contains(text(), 'SVP') or contains(text(), 'Director') or contains(text(), 'Lead')]")

    # Company Stats/Achievements
    STATS_SECTION = (By.CSS_SELECTOR, ".stats, .achievements, .milestones")
    STATS_ITEMS = (By.CSS_SELECTOR, ".stat-item, .achievement-item")

    # History/Timeline
    HISTORY_SECTION = (By.CSS_SELECTOR, ".history, .timeline, .journey")
    TIMELINE_ITEMS = (By.CSS_SELECTOR, ".timeline-item, .milestone")

    # Call to Action
    LETS_WORK_TOGETHER = (By.XPATH, "//*[contains(text(), \"Let's Work Together\")]")
    CTA_BUTTON = (By.XPATH, "//a[contains(text(), 'START NOW')]")

    # Images
    COMPANY_IMAGES = (By.CSS_SELECTOR, ".about-image, .company-image")
    TEAM_PHOTOS = (By.CSS_SELECTOR, ".team-photo, .member-photo")

    def __init__(self, driver: WebDriver):
        """Initialize AboutPage"""
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/about-us"
        logger.debug("AboutPage initialized")

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to_about_page(self):
        """Navigate to the about page"""
        self.navigate_to(self.url)
        logger.info(f"Navigated to about page: {self.url}")

    # ============================================
    # Content Interaction Methods
    # ============================================

    def get_page_title(self) -> str:
        """Get the about page title"""
        return self.get_text(self.PAGE_TITLE)

    def get_page_description(self) -> str:
        """Get the about page description"""
        return self.get_text(self.PAGE_DESCRIPTION)

    def is_mission_section_displayed(self) -> bool:
        """Check if mission section is displayed"""
        return self.is_element_displayed(self.MISSION_SECTION)

    def is_vision_section_displayed(self) -> bool:
        """Check if vision section is displayed"""
        return self.is_element_displayed(self.VISION_SECTION)

    def is_values_section_displayed(self) -> bool:
        """Check if values section is displayed"""
        return self.is_element_displayed(self.VALUES_SECTION)

    # ============================================
    # Team Section Methods
    # ============================================

    def is_team_section_displayed(self) -> bool:
        """Check if team section is displayed"""
        return self.is_element_displayed(self.TEAM_SECTION)

    def get_team_members_count(self) -> int:
        """Get the number of team members displayed"""
        members = self.find_elements(self.TEAM_MEMBERS)
        count = len(members)
        logger.info(f"Found {count} team members")
        return count

    def get_team_member_names(self) -> list:
        """Get list of team member names"""
        name_elements = self.find_elements(self.TEAM_MEMBER_NAMES)
        names = [elem.text for elem in name_elements if elem.text]
        logger.info(f"Retrieved {len(names)} team member names")
        return names

    def click_team_member(self, index: int = 0):
        """
        Click on a team member card

        Args:
            index: Index of the team member (default 0 for first)
        """
        members = self.find_elements(self.TEAM_MEMBERS)
        if members and len(members) > index:
            self.scroll_to_element(self.driver, members[index])
            members[index].click()
            logger.info(f"Clicked team member at index {index}")

    # ============================================
    # Stats/Achievements Methods
    # ============================================

    def is_stats_section_displayed(self) -> bool:
        """Check if stats/achievements section is displayed"""
        return self.is_element_displayed(self.STATS_SECTION)

    def get_stats_count(self) -> int:
        """Get the number of stats/achievements displayed"""
        stats = self.find_elements(self.STATS_ITEMS)
        count = len(stats)
        logger.info(f"Found {count} stats/achievements")
        return count

    # ============================================
    # History/Timeline Methods
    # ============================================

    def is_history_section_displayed(self) -> bool:
        """Check if history/timeline section is displayed"""
        return self.is_element_displayed(self.HISTORY_SECTION)

    def get_timeline_items_count(self) -> int:
        """Get the number of timeline items"""
        items = self.find_elements(self.TIMELINE_ITEMS)
        count = len(items)
        logger.info(f"Found {count} timeline items")
        return count

    # ============================================
    # CTA Methods
    # ============================================

    def click_cta_button(self):
        """Click the CTA button"""
        if self.is_element_displayed(self.CTA_BUTTON):
            self.scroll_to_element_locator(self.CTA_BUTTON)
            self.click(self.CTA_BUTTON)
            logger.info("Clicked CTA button")

    # ============================================
    # Validation Methods
    # ============================================

    def verify_about_page_loaded(self) -> bool:
        """Verify that about page is loaded successfully"""
        checks = [
            self.is_element_displayed(self.PAGE_TITLE),
            self.is_element_displayed(self.COMPANY_SECTION) or self.is_element_displayed(self.PAGE_DESCRIPTION),
        ]
        result = any(checks)

        if result:
            logger.info("✓ About page loaded successfully")
        else:
            logger.warning("✗ About page did not load properly")
            self.take_screenshot("about_page_load_failed")

        return result

    def verify_key_sections_present(self) -> dict:
        """
        Verify which key sections are present on the page

        Returns:
            dict: Dictionary with section names and their presence status
        """
        sections = {
            'mission': self.is_mission_section_displayed(),
            'vision': self.is_vision_section_displayed(),
            'values': self.is_values_section_displayed(),
            'team': self.is_team_section_displayed(),
            'stats': self.is_stats_section_displayed(),
            'history': self.is_history_section_displayed(),
        }

        present_count = sum(sections.values())
        logger.info(f"{present_count} out of {len(sections)} key sections are present")

        return sections
