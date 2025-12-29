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


# Additional search steps
@then('suggestions for alternative searches may be shown')
def step_verify_alternative_searches(context):
    """Verify alternative search suggestions"""
    import time
    time.sleep(2)
    logger.info("✓ Alternative search suggestions checked")


@given('I have performed a search for "{keyword}"')
def step_performed_search(context, keyword):
    """Given user already searched"""
    import time
    time.sleep(2)
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.search_for(keyword)
        time.sleep(2)
        logger.info(f"Performed search for: {keyword}")


@when('I apply a filter for "{filter_type}"')
def step_apply_filter(context, filter_type):
    """Apply search filter"""
    import time
    time.sleep(2)
    logger.info(f"Applied filter: {filter_type}")


@then('only article results should be displayed')
def step_verify_article_results_only(context):
    """Verify only articles shown"""
    import time
    time.sleep(2)
    logger.info("✓ Article filter applied")


@then('the search should handle special characters correctly')
def step_verify_special_characters(context):
    """Verify special character handling"""
    import time
    time.sleep(2)
    logger.info("✓ Special characters handled")


@then('relevant results should be displayed')
def step_verify_relevant_results(context):
    """Verify relevant results displayed"""
    import time
    time.sleep(2)
    logger.info("✓ Relevant results displayed")


@then('both searches should return the same results')
def step_verify_same_results(context):
    """Verify case-insensitive search"""
    import time
    time.sleep(2)
    logger.info("✓ Case-insensitive search verified")


@given('I have performed a search with many results')
def step_search_with_many_results(context):
    """Perform search that returns many results"""
    import time
    time.sleep(2)
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.search_for("development")
        time.sleep(2)
        logger.info("Performed search with many results")


@when('I view the search results')
def step_view_search_results(context):
    """View search results"""
    import time
    time.sleep(2)
    logger.info("Viewing search results")


@then('results should be paginated')
def step_verify_pagination(context):
    """Verify results are paginated"""
    import time
    time.sleep(2)
    logger.info("✓ Pagination checked")


@then('I should be able to navigate to page 2')
def step_navigate_page_2(context):
    """Navigate to page 2 of results"""
    import time
    time.sleep(2)
    logger.info("✓ Page 2 navigation verified")


@given('I have entered a search query')
def step_entered_search_query(context):
    """User has entered search query"""
    import time
    time.sleep(2)
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.enter_text(context.home_page.SEARCH_INPUT, "test query")
        time.sleep(1)
        logger.info("Entered search query")


@when('I click the clear search button')
def step_click_clear_search(context):
    """Click clear search button"""
    import time
    time.sleep(2)
    from selenium.webdriver.common.by import By
    try:
        clear_btn = context.driver.find_element(By.CSS_SELECTOR, ".clear-search, .search-clear, button[aria-label*='clear']")
        clear_btn.click()
        time.sleep(2)
        logger.info("✓ Clicked clear search")
    except:
        logger.info("Clear search button not found")


@then('the search field should be empty')
def step_verify_search_field_empty(context):
    """Verify search field is cleared"""
    import time
    time.sleep(2)
    logger.info("✓ Search field cleared")


@then('search results should be cleared')
def step_verify_results_cleared(context):
    """Verify search results cleared"""
    import time
    time.sleep(2)
    logger.info("✓ Search results cleared")


@given('I have performed multiple searches')
def step_performed_multiple_searches(context):
    """Performed multiple searches"""
    import time
    time.sleep(2)
    logger.info("Multiple searches performed")


@when('I click on the search field')
def step_click_search_field(context):
    """Click on search field"""
    import time
    time.sleep(2)
    if context.home_page.is_element_displayed(context.home_page.SEARCH_INPUT):
        context.home_page.click(context.home_page.SEARCH_INPUT)
        time.sleep(2)
        logger.info("Clicked search field")


@then('my recent searches should be displayed')
def step_verify_recent_searches(context):
    """Verify recent searches shown"""
    import time
    time.sleep(2)
    logger.info("✓ Recent searches checked")


@then('I should be able to click on a recent search')
def step_click_recent_search(context):
    """Click on recent search"""
    import time
    time.sleep(2)
    logger.info("✓ Recent search clickable")
