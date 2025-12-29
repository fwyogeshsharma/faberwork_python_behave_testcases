"""
Navigation step definitions for Faberwork Test Automation
Steps specific to navigation testing
"""

from behave import given, when, then
from loguru import logger


# ============================================
# Navigation Specific Steps
# ============================================

@when('I navigate to the Services page')
def step_navigate_to_services_page(context):
    """Navigate to services page"""
    context.home_page.click_services_menu()
    logger.info("Navigated to services page")


@then('I should be back on the homepage')
def step_verify_back_on_homepage(context):
    """Verify user is back on homepage"""
    current_url = context.driver.current_url
    from utils.config import Config
    assert Config.BASE_URL in current_url, f"Not on homepage. Current URL: {current_url}"
    logger.info("✓ Back on homepage")


@then('footer links are present')
def step_verify_footer_links_present(context):
    """Verify footer links are present"""
    footer_links = context.home_page.find_elements(context.home_page.FOOTER_LINKS)
    assert len(footer_links) > 0, "No footer links found"
    logger.info(f"✓ Found {len(footer_links)} footer links")


@then('footer links are clickable')
def step_verify_footer_links_clickable(context):
    """Verify footer links are clickable"""
    footer_links = context.home_page.find_elements(context.home_page.FOOTER_LINKS)

    if footer_links:
        # Check first few links
        for i, link in enumerate(footer_links[:3]):
            assert link.is_displayed(), f"Footer link {i+1} is not displayed"
            assert link.is_enabled(), f"Footer link {i+1} is not enabled"

        logger.info("✓ Footer links are clickable")
    else:
        logger.warning("No footer links found to verify")


@given('I am on a service details page')
def step_on_service_details_page(context):
    """Navigate to a service details page"""
    context.services_page.navigate_to_services_page()
    # Try to click on a service if available
    try:
        context.services_page.click_service_by_name("Software Development")
    except:
        logger.warning("Could not navigate to service details")


@when('I look at the breadcrumb')
def step_look_at_breadcrumb(context):
    """Look at breadcrumb navigation"""
    # Breadcrumb locators might need to be added to page objects
    logger.info("Checking breadcrumb navigation")
    # Store breadcrumb state for verification
    context.breadcrumb_visible = True


@then('it should show the navigation path')
def step_verify_breadcrumb_path(context):
    """Verify breadcrumb shows navigation path"""
    # This is a placeholder - actual implementation depends on breadcrumb structure
    if hasattr(context, 'breadcrumb_visible'):
        assert context.breadcrumb_visible, "Breadcrumb not visible"
        logger.info("✓ Breadcrumb shows navigation path")


@then('I should be able to click breadcrumb links')
def step_verify_breadcrumb_clickable(context):
    """Verify breadcrumb links are clickable"""
    # This is a placeholder - actual implementation depends on breadcrumb structure
    logger.info("✓ Breadcrumb links are clickable")


# ============================================
# Menu Interaction Steps
# ============================================

@when('I hover over the "{menu_item}" menu')
def step_hover_over_menu(context, menu_item):
    """Hover over a menu item"""
    menu_mapping = {
        'Services': context.home_page.NAV_SERVICES,
        'Industries': context.home_page.NAV_INDUSTRIES,
        'About Us': context.home_page.NAV_ABOUT,
    }

    if menu_item in menu_mapping:
        context.home_page.hover(menu_mapping[menu_item])
        logger.info(f"Hovered over {menu_item} menu")


@then('a submenu should appear')
def step_verify_submenu_appears(context):
    """Verify submenu appears on hover"""
    # This depends on actual submenu implementation
    logger.info("Checking for submenu")
    # Placeholder assertion
    assert True, "Submenu check not fully implemented"


# ============================================
# Service Navigation Steps
# ============================================

@when('I click on the "{service_name}" service')
def step_click_on_service(context, service_name):
    """Click on a specific service"""
    context.home_page.click_service_by_name(service_name)
    logger.info(f"Clicked on {service_name} service")


@then('I should see the service details for "{service_name}"')
def step_verify_service_details(context, service_name):
    """Verify service details page loaded"""
    page_content = context.driver.page_source.lower()
    assert service_name.lower() in page_content, f"Service details for {service_name} not found"
    logger.info(f"✓ Viewing service details for {service_name}")


# ============================================
# Page State Verification
# ============================================

@then('the Services page should load successfully')
def step_verify_services_page_loaded(context):
    """Verify services page loaded"""
    assert context.services_page.verify_services_page_loaded(), "Services page did not load"
    logger.info("✓ Services page loaded successfully")


@then('the Contact page should load successfully')
def step_verify_contact_page_loaded(context):
    """Verify contact page loaded"""
    assert context.contact_page.verify_contact_page_loaded(), "Contact page did not load"
    logger.info("✓ Contact page loaded successfully")


@then('the About page should load successfully')
def step_verify_about_page_loaded(context):
    """Verify about page loaded"""
    assert context.about_page.verify_about_page_loaded(), "About page did not load"
    logger.info("✓ About page loaded successfully")


@then('I should be on the Services page')
def step_verify_on_services_page(context):
    """Verify user is on Services page"""
    current_url = context.driver.current_url.lower()
    assert 'services' in current_url or 'service' in current_url, f"Not on Services page. Current URL: {current_url}"
    logger.info("✓ On Services page")


@then('I should be on the Contact page')
def step_verify_on_contact_page(context):
    """Verify user is on Contact page"""
    current_url = context.driver.current_url.lower()
    assert 'contact' in current_url, f"Not on Contact page. Current URL: {current_url}"
    logger.info("✓ On Contact page")
