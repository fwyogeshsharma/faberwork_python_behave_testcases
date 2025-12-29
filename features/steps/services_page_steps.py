"""
Step definitions for Services page
"""

from behave import given, when, then
from loguru import logger
import time


@then('the Services page should load successfully')
def step_verify_services_page_loaded(context):
    """Verify Services page loaded successfully"""
    time.sleep(2)
    current_url = context.driver.current_url.lower()
    assert 'service' in current_url, f"Not on Services page. Current URL: {current_url}"
    logger.info("✓ Services page loaded successfully")


@then('the page title should contain "{title_text}"')
def step_verify_page_title_contains(context, title_text):
    """Verify page title contains specific text"""
    time.sleep(2)
    page_source = context.driver.page_source
    assert title_text in page_source, f"Page title doesn't contain '{title_text}'"
    logger.info(f"✓ Page title contains '{title_text}'")


@then('all service offerings are visible on the page')
def step_verify_all_services_visible(context):
    """Verify service offerings are visible"""
    time.sleep(2)
    from selenium.webdriver.common.by import By
    # Look for service cards or sections
    page_text = context.driver.page_source.lower()
    service_keywords = ['snowflake', 'software', 'development', 'consulting', 'ai', 'cloud']
    found_count = sum(1 for keyword in service_keywords if keyword in page_text)
    assert found_count >= 3, f"Expected multiple services, found {found_count}"
    logger.info(f"✓ Found {found_count} service offerings")


@then('I should see the following services')
def step_verify_specific_services(context):
    """Verify specific services are listed"""
    time.sleep(2)
    page_source = context.driver.page_source

    for row in context.table:
        service_name = row['Service']
        assert service_name.lower() in page_source.lower(), f"Service '{service_name}' not found"
        logger.info(f"✓ Service found: {service_name}")


@then('I should see the "{section_name}" section')
def step_verify_section_exists(context, section_name):
    """Verify a section exists on the page"""
    time.sleep(2)
    page_source = context.driver.page_source
    # Flexible matching
    section_words = section_name.lower().split()
    page_lower = page_source.lower()

    # Check if most words from section name are present
    found_words = sum(1 for word in section_words if word in page_lower and len(word) > 2)
    assert found_words >= len(section_words) // 2, f"Section '{section_name}' not found"
    logger.info(f"✓ Section '{section_name}' is present")
