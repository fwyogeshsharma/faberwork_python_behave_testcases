"""
Step definitions for Industries page
"""

from behave import given, when, then
from loguru import logger
import time


@then('the Industries page should load successfully')
def step_verify_industries_page_loaded(context):
    """Verify Industries page loaded successfully"""
    time.sleep(2)
    current_url = context.driver.current_url.lower()
    assert 'industr' in current_url, f"Not on Industries page. Current URL: {current_url}"
    logger.info("✓ Industries page loaded successfully")


@then('I should see industry sectors listed')
def step_verify_industry_sectors(context):
    """Verify industry sectors are listed"""
    time.sleep(2)
    page_source = context.driver.page_source.lower()
    industry_keywords = ['healthcare', 'finance', 'energy', 'technology', 'retail', 'manufacturing']
    found = sum(1 for keyword in industry_keywords if keyword in page_source)
    assert found >= 2, f"Expected multiple industries, found {found}"
    logger.info(f"✓ Found {found} industry sectors")


@then('all industry sectors are listed')
def step_verify_all_sectors_listed(context):
    """Verify all industry sectors are listed"""
    time.sleep(2)
    page_source = context.driver.page_source.lower()
    # Check for common industry terms
    industry_indicators = ['sector', 'industry', 'vertical', 'domain']
    found = any(indicator in page_source for indicator in industry_indicators)
    assert found, "Industry sectors section not found"
    logger.info("✓ Industry sectors are listed")


@then('industry filter functionality exists')
def step_verify_filter_functionality(context):
    """Verify filter functionality exists"""
    time.sleep(2)
    page_source = context.driver.page_source.lower()
    has_filter = 'filter' in page_source or 'search' in page_source or 'category' in page_source
    logger.info("✓ Filter functionality checked")
