"""
Configuration management for Faberwork Test Automation
Loads settings from .env file and provides centralized config access
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
    logger.info(f"Loaded environment variables from {ENV_FILE}")
else:
    logger.warning(f".env file not found at {ENV_FILE}. Using system environment variables.")


class Config:
    """Central configuration class for test automation"""

    # ============================================
    # Application Settings
    # ============================================
    BASE_URL = os.getenv('BASE_URL', 'https://www.faberwork.com')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

    # ============================================
    # Browser Configuration
    # ============================================
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    WINDOW_SIZE = os.getenv('WINDOW_SIZE', '1920x1080')
    BROWSER_VERSION = os.getenv('BROWSER_VERSION', 'latest')

    # ============================================
    # Wait Times (in seconds)
    # ============================================
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    SCRIPT_TIMEOUT = int(os.getenv('SCRIPT_TIMEOUT', 30))

    # ============================================
    # Test Configuration
    # ============================================
    TAKE_SCREENSHOT_ON_FAILURE = os.getenv('TAKE_SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    RETRY_FAILED_TESTS = int(os.getenv('RETRY_FAILED_TESTS', 2))
    MAX_RETRY_ATTEMPTS = int(os.getenv('MAX_RETRY_ATTEMPTS', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 2))

    # ============================================
    # Reporting
    # ============================================
    ALLURE_RESULTS_DIR = BASE_DIR / os.getenv('ALLURE_RESULTS_DIR', 'reports')
    SCREENSHOT_DIR = BASE_DIR / os.getenv('SCREENSHOT_DIR', 'screenshots')
    LOG_DIR = BASE_DIR / os.getenv('LOG_DIR', 'logs')
    REPORT_TITLE = os.getenv('REPORT_TITLE', 'Faberwork Test Automation Report')

    # ============================================
    # Logging
    # ============================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CONSOLE_LOG_LEVEL = os.getenv('CONSOLE_LOG_LEVEL', 'INFO')
    FILE_LOG_LEVEL = os.getenv('FILE_LOG_LEVEL', 'DEBUG')
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # ============================================
    # Selenium Grid (Optional)
    # ============================================
    USE_SELENIUM_GRID = os.getenv('USE_SELENIUM_GRID', 'False').lower() == 'true'
    SELENIUM_HUB_URL = os.getenv('SELENIUM_HUB_URL', 'http://selenium-hub:4444/wd/hub')

    # ============================================
    # Test Data
    # ============================================
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'test@example.com')
    TEST_USER_NAME = os.getenv('TEST_USER_NAME', 'Test User')
    TEST_COMPANY = os.getenv('TEST_COMPANY', 'Test Company')
    TEST_PHONE = os.getenv('TEST_PHONE', '+1234567890')

    # ============================================
    # API Configuration
    # ============================================
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://www.faberwork.com/api')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))

    # ============================================
    # Parallel Execution
    # ============================================
    PARALLEL_PROCESSES = int(os.getenv('PARALLEL_PROCESSES', 1))
    PARALLEL_ENABLED = os.getenv('PARALLEL_ENABLED', 'False').lower() == 'true'

    # ============================================
    # Email Notifications
    # ============================================
    SEND_EMAIL_REPORT = os.getenv('SEND_EMAIL_REPORT', 'False').lower() == 'true'
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', 'qa-team@example.com')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

    # ============================================
    # Slack Notifications
    # ============================================
    SEND_SLACK_NOTIFICATION = os.getenv('SEND_SLACK_NOTIFICATION', 'False').lower() == 'true'
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')

    # ============================================
    # Advanced Settings
    # ============================================
    CLEAR_COOKIES_BETWEEN_SCENARIOS = os.getenv('CLEAR_COOKIES_BETWEEN_SCENARIOS', 'True').lower() == 'true'
    CLEAR_CACHE_BETWEEN_SCENARIOS = os.getenv('CLEAR_CACHE_BETWEEN_SCENARIOS', 'False').lower() == 'true'
    ENABLE_PERFORMANCE_LOGGING = os.getenv('ENABLE_PERFORMANCE_LOGGING', 'False').lower() == 'true'
    ENABLE_NETWORK_LOGGING = os.getenv('ENABLE_NETWORK_LOGGING', 'False').lower() == 'true'
    ENABLE_BROWSER_LOGGING = os.getenv('ENABLE_BROWSER_LOGGING', 'True').lower() == 'true'

    # ============================================
    # Chrome Options
    # ============================================
    DISABLE_GPU = os.getenv('DISABLE_GPU', 'True').lower() == 'true'
    NO_SANDBOX = os.getenv('NO_SANDBOX', 'True').lower() == 'true'
    DISABLE_DEV_SHM_USAGE = os.getenv('DISABLE_DEV_SHM_USAGE', 'True').lower() == 'true'
    DISABLE_EXTENSIONS = os.getenv('DISABLE_EXTENSIONS', 'True').lower() == 'true'
    DISABLE_INFOBARS = os.getenv('DISABLE_INFOBARS', 'True').lower() == 'true'

    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.ALLURE_RESULTS_DIR,
            cls.SCREENSHOT_DIR,
            cls.LOG_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

    @classmethod
    def get_window_size(cls):
        """Parse and return window size as tuple (width, height)"""
        try:
            width, height = cls.WINDOW_SIZE.split('x')
            return int(width), int(height)
        except (ValueError, AttributeError):
            logger.warning(f"Invalid WINDOW_SIZE format: {cls.WINDOW_SIZE}. Using default 1920x1080")
            return 1920, 1080

    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)"""
        logger.info("=" * 60)
        logger.info("Current Test Configuration")
        logger.info("=" * 60)
        logger.info(f"BASE_URL: {cls.BASE_URL}")
        logger.info(f"ENVIRONMENT: {cls.ENVIRONMENT}")
        logger.info(f"BROWSER: {cls.BROWSER}")
        logger.info(f"HEADLESS: {cls.HEADLESS}")
        logger.info(f"WINDOW_SIZE: {cls.WINDOW_SIZE}")
        logger.info(f"IMPLICIT_WAIT: {cls.IMPLICIT_WAIT}s")
        logger.info(f"EXPLICIT_WAIT: {cls.EXPLICIT_WAIT}s")
        logger.info(f"SCREENSHOT_ON_FAILURE: {cls.TAKE_SCREENSHOT_ON_FAILURE}")
        logger.info(f"USE_SELENIUM_GRID: {cls.USE_SELENIUM_GRID}")
        logger.info("=" * 60)

    @classmethod
    def is_local_execution(cls):
        """Check if tests are running locally (not in Docker)"""
        return not os.path.exists('/.dockerenv')


# Initialize directories on module load
Config.create_directories()
