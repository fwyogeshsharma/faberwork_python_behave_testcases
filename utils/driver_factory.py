"""
WebDriver Factory for Faberwork Test Automation
Handles browser initialization with proper configurations
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from loguru import logger
from .config import Config


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    def create_driver(browser=None):
        """
        Create and configure WebDriver instance

        Args:
            browser (str): Browser type ('chrome', 'firefox', 'edge')

        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser or Config.BROWSER
        logger.info(f"Creating {browser} WebDriver instance")

        if browser.lower() == 'chrome':
            return DriverFactory._create_chrome_driver()
        elif browser.lower() == 'firefox':
            return DriverFactory._create_firefox_driver()
        elif browser.lower() == 'edge':
            return DriverFactory._create_edge_driver()
        else:
            logger.error(f"Unsupported browser: {browser}. Defaulting to Chrome.")
            return DriverFactory._create_chrome_driver()

    @staticmethod
    def _create_chrome_driver():
        """Create Chrome WebDriver with configurations"""
        chrome_options = ChromeOptions()

        # Headless mode
        if Config.HEADLESS:
            chrome_options.add_argument('--headless=new')
            logger.info("Chrome running in headless mode")

        # Window size
        width, height = Config.get_window_size()
        chrome_options.add_argument(f'--window-size={width},{height}')

        # Performance and stability options
        if Config.NO_SANDBOX:
            chrome_options.add_argument('--no-sandbox')

        if Config.DISABLE_DEV_SHM_USAGE:
            chrome_options.add_argument('--disable-dev-shm-usage')

        if Config.DISABLE_GPU:
            chrome_options.add_argument('--disable-gpu')

        if Config.DISABLE_EXTENSIONS:
            chrome_options.add_argument('--disable-extensions')

        if Config.DISABLE_INFOBARS:
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

        # Additional stability options
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-web-security')

        # Performance optimizations for parallel execution
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-breakpad')
        chrome_options.add_argument('--disable-component-extensions-with-background-pages')
        chrome_options.add_argument('--disable-features=TranslateUI,BlinkGenPropertyTrees')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        chrome_options.add_argument('--force-color-profile=srgb')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--mute-audio')

        # Memory and resource optimization
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-domain-reliability')
        chrome_options.add_argument('--disable-component-update')

        # User agent (avoid bot detection)
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Logging preferences
        if Config.ENABLE_BROWSER_LOGGING:
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--v=1')

        # Performance logging
        if Config.ENABLE_PERFORMANCE_LOGGING:
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # Network logging
        if Config.ENABLE_NETWORK_LOGGING:
            chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        # Preferences
        from pathlib import Path
        base_dir = Path(__file__).resolve().parent.parent
        prefs = {
            'download.default_directory': str(base_dir / 'downloads'),
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'profile.default_content_setting_values.notifications': 2,
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
        }
        chrome_options.add_experimental_option('prefs', prefs)

        try:
            # Use Selenium Grid if configured
            if Config.USE_SELENIUM_GRID:
                logger.info(f"Connecting to Selenium Grid at {Config.SELENIUM_HUB_URL}")
                driver = webdriver.Remote(
                    command_executor=Config.SELENIUM_HUB_URL,
                    options=chrome_options
                )
            else:
                # Local execution - try with automatic ChromeDriver download
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    from webdriver_manager.core.os_manager import ChromeType

                    # Try to install ChromeDriver
                    driver_path = ChromeDriverManager().install()
                    service = ChromeService(executable_path=driver_path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                except Exception as e:
                    logger.warning(f"webdriver-manager failed: {e}, trying direct Chrome instantiation")
                    # Fallback: try direct instantiation (Selenium 4.6+ can auto-download)
                    driver = webdriver.Chrome(options=chrome_options)

            # Set timeouts (increased for parallel execution stability)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            # Use higher page load timeout to handle parallel execution load
            page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', Config.PAGE_LOAD_TIMEOUT))
            driver.set_page_load_timeout(max(page_load_timeout, 90))  # Minimum 90s for parallel runs
            driver.set_script_timeout(Config.SCRIPT_TIMEOUT)

            logger.info("Chrome WebDriver created successfully")
            return driver

        except Exception as e:
            logger.error(f"Failed to create Chrome WebDriver: {str(e)}")
            raise

    @staticmethod
    def _create_firefox_driver():
        """Create Firefox WebDriver with configurations"""
        firefox_options = FirefoxOptions()

        # Headless mode
        if Config.HEADLESS:
            firefox_options.add_argument('--headless')
            logger.info("Firefox running in headless mode")

        # Window size
        width, height = Config.get_window_size()
        firefox_options.add_argument(f'--width={width}')
        firefox_options.add_argument(f'--height={height}')

        # Additional options
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--no-sandbox')

        # Preferences
        firefox_options.set_preference('dom.webnotifications.enabled', False)
        firefox_options.set_preference('dom.push.enabled', False)

        try:
            if Config.USE_SELENIUM_GRID:
                logger.info(f"Connecting to Selenium Grid at {Config.SELENIUM_HUB_URL}")
                driver = webdriver.Remote(
                    command_executor=Config.SELENIUM_HUB_URL,
                    options=firefox_options
                )
            else:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=firefox_options)

            # Set timeouts (increased for parallel execution stability)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            # Use higher page load timeout to handle parallel execution load
            page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', Config.PAGE_LOAD_TIMEOUT))
            driver.set_page_load_timeout(max(page_load_timeout, 90))  # Minimum 90s for parallel runs
            driver.set_script_timeout(Config.SCRIPT_TIMEOUT)

            logger.info("Firefox WebDriver created successfully")
            return driver

        except Exception as e:
            logger.error(f"Failed to create Firefox WebDriver: {str(e)}")
            raise

    @staticmethod
    def _create_edge_driver():
        """Create Edge WebDriver with configurations"""
        edge_options = EdgeOptions()

        # Headless mode
        if Config.HEADLESS:
            edge_options.add_argument('--headless')
            logger.info("Edge running in headless mode")

        # Window size
        width, height = Config.get_window_size()
        edge_options.add_argument(f'--window-size={width},{height}')

        # Additional options
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')

        try:
            if Config.USE_SELENIUM_GRID:
                logger.info(f"Connecting to Selenium Grid at {Config.SELENIUM_HUB_URL}")
                driver = webdriver.Remote(
                    command_executor=Config.SELENIUM_HUB_URL,
                    options=edge_options
                )
            else:
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=edge_options)

            # Set timeouts (increased for parallel execution stability)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            # Use higher page load timeout to handle parallel execution load
            page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', Config.PAGE_LOAD_TIMEOUT))
            driver.set_page_load_timeout(max(page_load_timeout, 90))  # Minimum 90s for parallel runs
            driver.set_script_timeout(Config.SCRIPT_TIMEOUT)

            logger.info("Edge WebDriver created successfully")
            return driver

        except Exception as e:
            logger.error(f"Failed to create Edge WebDriver: {str(e)}")
            raise

    @staticmethod
    def quit_driver(driver):
        """
        Safely quit WebDriver instance

        Args:
            driver: WebDriver instance to quit
        """
        try:
            if driver:
                driver.quit()
                logger.info("WebDriver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting WebDriver: {str(e)}")
