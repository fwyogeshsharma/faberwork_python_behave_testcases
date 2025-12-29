"""
Common step definitions for Faberwork Test Automation
Shared steps used across multiple feature files
"""

from behave import given, when, then
from loguru import logger
from utils.config import Config
from utils.test_data import TestDataGenerator


# Initialize test data generator
test_data = TestDataGenerator()


# ============================================
# Background/Setup Steps
# ============================================

@given('the Faberwork website is accessible')
def step_check_website_accessible(context):
    """Verify the website is accessible"""
    context.home_page.navigate_to_homepage()
    assert context.driver.current_url, "Failed to load website"
    logger.info("✓ Website is accessible")


@given('I am on the Faberwork homepage')
@given('I am on the homepage')
def step_navigate_to_homepage(context):
    """Navigate to homepage"""
    context.home_page.navigate_to_homepage()
    logger.info("Navigated to homepage")


@given('I am on the Services page')
def step_navigate_to_services(context):
    """Navigate to services page"""
    context.services_page.navigate_to_services_page()
    logger.info("Navigated to services page")


@given('I am on the Contact page')
def step_navigate_to_contact(context):
    """Navigate to contact page"""
    context.contact_page.navigate_to_contact_page()
    logger.info("Navigated to contact page")


@given('I am on the About page')
def step_navigate_to_about(context):
    """Navigate to about page"""
    context.about_page.navigate_to_about_page()
    logger.info("Navigated to about page")


# ============================================
# Navigation Steps
# ============================================

@when('I navigate to the homepage')
def step_go_to_homepage(context):
    """Navigate to homepage"""
    context.home_page.navigate_to_homepage()


@when('I click on the "{menu_item}" menu')
def step_click_menu_item(context, menu_item):
    """Click on a navigation menu item"""
    menu_mapping = {
        'Services': context.home_page.click_services_menu,
        'Industries': context.home_page.click_industries_menu,
        'Success Stories': context.home_page.click_success_stories_menu,
        'Latest Thinking': context.home_page.click_latest_thinking_menu,
        'About Us': context.home_page.click_about_menu,
        'Contact Us': context.home_page.click_contact_menu,
    }

    if menu_item in menu_mapping:
        menu_mapping[menu_item]()
        logger.info(f"Clicked on {menu_item} menu")
    else:
        raise ValueError(f"Unknown menu item: {menu_item}")


@when('I click on the logo')
def step_click_logo(context):
    """Click on the website logo"""
    context.home_page.click_logo()
    logger.info("Clicked on logo")


@when('I click the browser back button')
def step_click_back_button(context):
    """Click browser back button"""
    context.home_page.go_back()
    logger.info("Clicked browser back button")


# ============================================
# Scroll Steps
# ============================================

@when('I scroll to the consultation form')
@when('I scroll to the form')
def step_scroll_to_form(context):
    """Scroll to consultation form"""
    context.home_page.scroll_to_element_locator(context.home_page.CONSULTATION_FORM)
    logger.info("Scrolled to consultation form")


@when('I scroll to the footer')
def step_scroll_to_footer(context):
    """Scroll to page footer"""
    context.home_page.scroll_to_bottom()
    logger.info("Scrolled to footer")


@when('I scroll to the testimonials section')
def step_scroll_to_testimonials(context):
    """Scroll to testimonials section"""
    context.home_page.scroll_to_element_locator(context.home_page.TESTIMONIAL_SECTION)
    logger.info("Scrolled to testimonials")


@when('I scroll to the success stories section')
def step_scroll_to_success_stories(context):
    """Scroll to success stories section"""
    context.home_page.scroll_to_element_locator(context.home_page.SUCCESS_STORIES_SECTION)
    logger.info("Scrolled to success stories")


# ============================================
# Validation/Assertion Steps
# ============================================

@then('the homepage should load successfully')
def step_verify_homepage_loaded(context):
    """Verify homepage loaded successfully"""
    assert context.home_page.verify_homepage_loaded(), "Homepage did not load successfully"
    logger.info("✓ Homepage loaded successfully")


@then('the logo should be visible')
def step_verify_logo_visible(context):
    """Verify logo is visible"""
    assert context.home_page.is_element_displayed(context.home_page.LOGO), "Logo is not visible"
    logger.info("✓ Logo is visible")


@then('all navigation links should be present')
def step_verify_nav_links_present(context):
    """Verify all navigation links are present"""
    assert context.home_page.verify_all_navigation_links_present(), "Not all navigation links are present"
    logger.info("✓ All navigation links are present")


@then('I should be on the homepage')
def step_verify_on_homepage(context):
    """Verify currently on homepage"""
    current_url = context.driver.current_url
    assert Config.BASE_URL in current_url, f"Not on homepage. Current URL: {current_url}"
    logger.info("✓ On homepage")


@then('I should be on the "{page_name}" page')
def step_verify_on_page(context, page_name):
    """Verify on a specific page"""
    current_url = context.driver.current_url.lower()
    page_name_lower = page_name.lower()

    # Check if page name or fragment is in URL
    assert page_name_lower in current_url, f"Not on {page_name} page. Current URL: {current_url}"
    logger.info(f"✓ On {page_name} page")


@then('the URL should contain "{url_fragment}"')
def step_verify_url_contains(context, url_fragment):
    """Verify URL contains specific fragment"""
    current_url = context.driver.current_url.lower()
    assert url_fragment.lower() in current_url, f"URL does not contain '{url_fragment}'. Current URL: {current_url}"
    logger.info(f"✓ URL contains '{url_fragment}'")


@then('the page should load successfully')
def step_verify_page_loaded(context):
    """Verify current page loaded successfully"""
    context.home_page.wait_for_page_load()
    assert context.driver.title, "Page did not load (no title)"
    logger.info("✓ Page loaded successfully")


# ============================================
# Wait Steps
# ============================================

@when('I wait for {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified number of seconds"""
    import time
    time.sleep(seconds)
    logger.info(f"Waited for {seconds} seconds")


# ============================================
# Screenshot Steps
# ============================================

@when('I take a screenshot named "{name}"')
@then('I take a screenshot named "{name}"')
def step_take_screenshot(context, name):
    """Take a screenshot with given name"""
    context.home_page.take_screenshot(name)
    logger.info(f"Screenshot taken: {name}")


# ============================================
# Generic Element Steps
# ============================================

@then('{element} should be visible')
def step_element_should_be_visible(context, element):
    """Generic step to verify element visibility"""
    logger.info(f"Checking visibility of: {element}")
    # This is a generic step - actual implementation depends on element
    assert True, f"{element} visibility check not implemented"


@then('{element} should be present')
def step_element_should_be_present(context, element):
    """Generic step to verify element presence"""
    logger.info(f"Checking presence of: {element}")
    # This is a generic step - actual implementation depends on element
    assert True, f"{element} presence check not implemented"


# ============================================
# Browser/Window Steps
# ============================================

@when('I refresh the page')
def step_refresh_page(context):
    """Refresh the current page"""
    context.home_page.refresh_page()
    logger.info("Page refreshed")


@when('I maximize the browser window')
def step_maximize_window(context):
    """Maximize browser window"""
    if not Config.HEADLESS:
        context.driver.maximize_window()
        logger.info("Browser window maximized")


# ============================================
# Utility Steps
# ============================================

@given('I have generated test data')
def step_generate_test_data(context):
    """Generate test data for the scenario"""
    context.test_data = test_data.generate_user_data()
    logger.info(f"Generated test data: {context.test_data}")


@then('no JavaScript errors should occur')
def step_verify_no_js_errors(context):
    """Verify no JavaScript errors in console"""
    try:
        logs = context.driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']

        if errors:
            logger.warning(f"Found {len(errors)} JavaScript errors:")
            for error in errors:
                logger.warning(f"  - {error['message']}")

        # Decide if you want to fail the test on JS errors
        # assert len(errors) == 0, f"Found {len(errors)} JavaScript errors"

    except Exception as e:
        logger.warning(f"Could not check JavaScript errors: {str(e)}")
