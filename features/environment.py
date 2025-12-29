"""
Behave Environment Configuration for Faberwork Test Automation
Defines hooks and setup/teardown logic for test execution
"""

import sys
import io
from pathlib import Path

# Ensure UTF-8 encoding for stdout to handle Unicode characters on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime
from loguru import logger

from utils.config import Config
from utils.driver_factory import DriverFactory
from pages.home_page import HomePage
from pages.services_page import ServicesPage
from pages.contact_page import ContactPage
from pages.about_page import AboutPage


# ============================================
# Configure Loguru Logger
# ============================================
def configure_logger():
    """Configure logging for the test run"""
    # Remove default logger
    logger.remove()

    # Console logging (stdout already configured with UTF-8 encoding)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=Config.CONSOLE_LOG_LEVEL,
        colorize=True
    )

    # File logging
    log_file = Config.LOG_DIR / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=Config.FILE_LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    logger.info("=" * 80)
    logger.info("Test Execution Started")
    logger.info("=" * 80)


# ============================================
# Before All Hook
# ============================================
def before_all(context):
    """
    Runs once before all tests
    Setup global configuration and logging
    """
    # Configure logging
    configure_logger()

    # Print configuration
    Config.print_config()

    # Initialize test statistics
    context.test_stats = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'start_time': datetime.now()
    }

    logger.info("Global setup completed")


# ============================================
# Before Feature Hook
# ============================================
def before_feature(context, feature):
    """
    Runs before each feature file

    Args:
        context: Behave context
        feature: Feature being executed
    """
    logger.info("=" * 80)
    logger.info(f"Starting Feature: {feature.name}")
    logger.info(f"Description: {feature.description if feature.description else 'N/A'}")
    logger.info(f"Tags: {feature.tags if feature.tags else 'None'}")
    logger.info("=" * 80)


# ============================================
# Before Scenario Hook
# ============================================
def before_scenario(context, scenario):
    """
    Runs before each scenario
    Initialize WebDriver and page objects

    Args:
        context: Behave context
        scenario: Scenario being executed
    """
    logger.info("-" * 80)
    logger.info(f"Starting Scenario: {scenario.name}")
    logger.info(f"Tags: {scenario.tags if scenario.tags else 'None'}")
    logger.info("-" * 80)

    try:
        # Create WebDriver instance
        context.driver = DriverFactory.create_driver()
        logger.info("WebDriver created successfully")

        # Initialize page objects
        context.home_page = HomePage(context.driver)
        context.services_page = ServicesPage(context.driver)
        context.contact_page = ContactPage(context.driver)
        context.about_page = AboutPage(context.driver)
        logger.info("Page objects initialized")

        # Maximize window
        if not Config.HEADLESS:
            context.driver.maximize_window()

        # Update statistics
        context.test_stats['total'] += 1

    except Exception as e:
        logger.error(f"Failed to setup scenario: {str(e)}")
        raise


# ============================================
# After Scenario Hook
# ============================================
def after_scenario(context, scenario):
    """
    Runs after each scenario
    Take screenshots on failure and cleanup

    Args:
        context: Behave context
        scenario: Scenario that was executed
    """
    try:
        # Check scenario status
        if scenario.status == 'failed':
            logger.error(f"✗ Scenario FAILED: {scenario.name}")
            context.test_stats['failed'] += 1

            # Take screenshot on failure
            if Config.TAKE_SCREENSHOT_ON_FAILURE and hasattr(context, 'driver'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"FAILED_{scenario.name.replace(' ', '_')}_{timestamp}"
                screenshot_path = Config.SCREENSHOT_DIR / f"{screenshot_name}.png"

                context.driver.save_screenshot(str(screenshot_path))
                logger.info(f"Screenshot saved: {screenshot_path}")

                # Attach screenshot to Allure report (if using Allure)
                try:
                    import allure
                    allure.attach.file(
                        str(screenshot_path),
                        name=screenshot_name,
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass  # Allure not installed

        elif scenario.status == 'passed':
            logger.info(f"✓ Scenario PASSED: {scenario.name}")
            context.test_stats['passed'] += 1

        elif scenario.status == 'skipped':
            logger.warning(f"⊘ Scenario SKIPPED: {scenario.name}")
            context.test_stats['skipped'] += 1

        # Clear cookies if configured
        if Config.CLEAR_COOKIES_BETWEEN_SCENARIOS and hasattr(context, 'driver'):
            context.driver.delete_all_cookies()
            logger.debug("Cookies cleared")

    except Exception as e:
        logger.error(f"Error in after_scenario hook: {str(e)}")

    finally:
        # Quit driver
        if hasattr(context, 'driver'):
            try:
                DriverFactory.quit_driver(context.driver)
            except Exception as e:
                logger.error(f"Error quitting driver: {str(e)}")

    logger.info("-" * 80)
    logger.info(f"Completed Scenario: {scenario.name} - Status: {str(scenario.status).upper()}")
    logger.info("-" * 80)


# ============================================
# After Feature Hook
# ============================================
def after_feature(context, feature):
    """
    Runs after each feature file

    Args:
        context: Behave context
        feature: Feature that was executed
    """
    logger.info("=" * 80)
    logger.info(f"Completed Feature: {feature.name}")
    logger.info(f"Feature Status: {str(feature.status).upper()}")
    logger.info("=" * 80)


# ============================================
# After All Hook
# ============================================
def after_all(context):
    """
    Runs once after all tests
    Print test summary and cleanup
    """
    # Calculate execution time
    end_time = datetime.now()
    duration = end_time - context.test_stats['start_time']

    # Print test summary
    logger.info("=" * 80)
    logger.info("TEST EXECUTION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Scenarios: {context.test_stats['total']}")
    logger.info(f"✓ Passed: {context.test_stats['passed']}")
    logger.info(f"✗ Failed: {context.test_stats['failed']}")
    logger.info(f"⊘ Skipped: {context.test_stats['skipped']}")
    logger.info(f"Execution Time: {duration}")
    logger.info(f"Success Rate: {(context.test_stats['passed'] / context.test_stats['total'] * 100):.2f}%" if context.test_stats['total'] > 0 else "N/A")
    logger.info("=" * 80)

    # Log completion
    logger.info("Test Execution Completed")
    logger.info("=" * 80)


# ============================================
# Step Hooks (Optional)
# ============================================
def before_step(context, step):
    """
    Runs before each step (optional - can be removed if too verbose)

    Args:
        context: Behave context
        step: Step being executed
    """
    logger.debug(f"→ Step: {step.keyword} {step.name}")


def after_step(context, step):
    """
    Runs after each step (optional)

    Args:
        context: Behave context
        step: Step that was executed
    """
    if step.status == 'failed':
        logger.error(f"✗ Step failed: {step.keyword} {step.name}")
    else:
        logger.debug(f"✓ Step passed: {step.keyword} {step.name}")


# ============================================
# Tag Handling (Optional)
# ============================================
def before_tag(context, tag):
    """
    Handle specific tags before scenario execution

    Args:
        context: Behave context
        tag: Tag being processed
    """
    if tag == 'skip':
        context.scenario.skip("Skipped due to @skip tag")
    elif tag == 'slow':
        logger.warning("This is a slow test - may take longer to execute")


# ============================================
# Custom Utility Functions
# ============================================
def attach_log_to_allure(log_message: str, name: str = "Log"):
    """
    Attach log message to Allure report

    Args:
        log_message: Message to attach
        name: Attachment name
    """
    try:
        import allure
        allure.attach(
            log_message,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
    except ImportError:
        pass  # Allure not installed
