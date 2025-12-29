"""
Page Objects module for Faberwork Test Automation
Contains all page object classes following POM pattern
"""

from .base_page import BasePage
from .home_page import HomePage
from .services_page import ServicesPage
from .contact_page import ContactPage
from .about_page import AboutPage

__all__ = [
    'BasePage',
    'HomePage',
    'ServicesPage',
    'ContactPage',
    'AboutPage',
]
