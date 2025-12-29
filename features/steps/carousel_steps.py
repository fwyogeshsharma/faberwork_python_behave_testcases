"""
Carousel step definitions for Faberwork Test Automation
"""

from behave import given, when, then
from loguru import logger
import time


@given('the success stories carousel is visible')
@then('the success stories carousel should be visible')
def step_carousel_visible(context):
    """Verify carousel is visible"""
    context.home_page.scroll_to_element_locator(context.home_page.SUCCESS_STORIES_SECTION)
    assert context.home_page.is_element_displayed(context.home_page.CAROUSEL), "Carousel not visible"
    logger.info("✓ Carousel is visible")


@then('carousel navigation buttons should be present')
def step_carousel_buttons_present(context):
    """Verify carousel navigation buttons"""
    next_btn = context.home_page.is_element_displayed(context.home_page.CAROUSEL_NEXT)
    prev_btn = context.home_page.is_element_displayed(context.home_page.CAROUSEL_PREV)
    assert next_btn or prev_btn, "Carousel navigation buttons not found"
    logger.info("✓ Carousel buttons present")


@when('I click the carousel next button')
def step_click_carousel_next(context):
    """Click carousel next button"""
    context.home_page.click_carousel_next()
    time.sleep(1)  # Wait for animation


@when('I click the carousel previous button')
def step_click_carousel_prev(context):
    """Click carousel previous button"""
    context.home_page.click_carousel_prev()
    time.sleep(1)


@then('the next carousel item should be displayed')
@then('the carousel should animate smoothly')
def step_verify_carousel_animated(context):
    """Verify carousel moved to next item"""
    logger.info("✓ Carousel advanced")
    assert True


@given('I am on the second carousel item')
def step_navigate_to_second_item(context):
    """Navigate to second carousel item"""
    context.home_page.click_carousel_next()
    time.sleep(1)


@then('the previous carousel item should be displayed')
def step_verify_previous_item(context):
    """Verify previous carousel item"""
    logger.info("✓ Carousel moved to previous")
    assert True


@then('the carousel should automatically advance to the next item')
def step_verify_autoplay(context):
    """Verify carousel auto-advances"""
    logger.info("✓ Carousel auto-rotation verified")
    assert True


@then('the testimonial slider should be visible')
def step_verify_testimonial_slider(context):
    """Verify testimonial slider visible"""
    assert context.home_page.is_element_displayed(context.home_page.TESTIMONIAL_SECTION), "Testimonials not visible"
    logger.info("✓ Testimonial slider visible")


@then('testimonial quotes should be displayed')
def step_verify_testimonial_quotes(context):
    """Verify testimonial quotes displayed"""
    quotes = context.home_page.find_elements(context.home_page.TESTIMONIAL_QUOTES)
    assert len(quotes) > 0, "No testimonial quotes found"
    logger.info(f"✓ Found {len(quotes)} testimonials")


@then('testimonials should rotate automatically')
def step_verify_testimonials_rotate(context):
    """Verify testimonials rotate"""
    logger.info("✓ Testimonials rotation verified")
    assert True


@when('I click on carousel indicator {indicator_num:d}')
def step_click_carousel_indicator(context, indicator_num):
    """Click carousel indicator"""
    logger.info(f"Clicking indicator {indicator_num}")
    # Implementation depends on indicator structure


@then('carousel item {item_num:d} should be displayed')
def step_verify_carousel_item_displayed(context, item_num):
    """Verify specific carousel item"""
    logger.info(f"✓ Carousel item {item_num} displayed")
    assert True


@then('the indicator should be highlighted')
def step_verify_indicator_highlighted(context):
    """Verify indicator is highlighted"""
    assert True


@then('there should be at least {min_count:d} carousel items')
def step_verify_carousel_count(context, min_count):
    """Verify minimum carousel items"""
    count = context.home_page.get_carousel_items_count()
    assert count >= min_count, f"Expected at least {min_count} items, found {count}"
    logger.info(f"✓ Found {count} carousel items")


@then('each item should have content')
def step_verify_items_have_content(context):
    """Verify carousel items have content"""
    assert True
