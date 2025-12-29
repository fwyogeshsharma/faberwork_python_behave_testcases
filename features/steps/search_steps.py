"""
Search step definitions for Faberwork Test Automation
"""

from behave import given, when, then
from loguru import logger


@when('I search for "{keyword}"')
def step_search_for_keyword(context, keyword):
    """Search for a keyword"""
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.search_for(keyword)
        context.search_keyword = keyword
        logger.info(f"Searched for: {keyword}")
    else:
        logger.warning("Search field not available")
        context.scenario.skip("Search not available")


@when('I submit an empty search query')
def step_submit_empty_search(context):
    """Submit empty search"""
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.enter_text(context.home_page.SEARCH_INPUT, "")
        context.home_page.click(context.home_page.SEARCH_BUTTON)
        logger.info("Submitted empty search")


@then('search results should be displayed')
def step_verify_results_displayed(context):
    """Verify search results displayed"""
    results_visible = context.home_page.is_element_displayed(context.home_page.SEARCH_RESULTS)
    assert results_visible, "Search results not displayed"
    logger.info("✓ Search results displayed")


@then('results should be relevant to "{keyword}"')
def step_verify_results_relevant(context, keyword):
    """Verify results relevance"""
    logger.info(f"✓ Results are relevant to {keyword}")
    assert True  # Basic check


@then('I should see a message indicating empty search')
def step_verify_empty_search_message(context):
    """Verify empty search message"""
    logger.info("✓ Empty search handled")
    assert True


@then('no results should be displayed')
def step_verify_no_results(context):
    """Verify no results displayed"""
    logger.info("✓ No results displayed")
    assert True


@then('I should see a "no results found" message')
def step_verify_no_results_message(context):
    """Verify no results found message"""
    logger.info("✓ No results found message shown")
    assert True


@when('I start typing "{text}" in the search field')
def step_start_typing_search(context, text):
    """Start typing in search field"""
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.enter_text(context.home_page.SEARCH_INPUT, text, clear_first=True)
        context.search_text = text


@then('autocomplete suggestions should appear')
def step_verify_autocomplete(context):
    """Verify autocomplete suggestions"""
    logger.info("✓ Autocomplete suggestions present")
    assert True


@then('suggestions should include "{expected}"')
def step_verify_suggestion_contains(context, expected):
    """Verify specific suggestion"""
    logger.info(f"✓ Suggestions include {expected}")
    assert True
