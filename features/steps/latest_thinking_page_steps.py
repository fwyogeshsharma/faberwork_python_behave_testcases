"""
Step definitions for Latest Thinking page
"""

from behave import given, when, then
from loguru import logger
import time


@then('the Latest Thinking page should load successfully')
def step_verify_latest_thinking_page_loaded(context):
    """Verify Latest Thinking page loaded successfully"""
    time.sleep(2)
    current_url = context.driver.current_url.lower()
    assert 'thinking' in current_url or 'blog' in current_url or 'article' in current_url, \
        f"Not on Latest Thinking page. Current URL: {current_url}"
    logger.info("✓ Latest Thinking page loaded successfully")


@then('I should see blog posts or articles')
def step_verify_blog_posts(context):
    """Verify blog posts are present"""
    time.sleep(2)
    page_source = context.driver.page_source.lower()
    content_indicators = ['article', 'post', 'blog', 'read', 'thinking']
    found = sum(1 for indicator in content_indicators if indicator in page_source)
    assert found >= 2, f"Blog content not found adequately"
    logger.info("✓ Blog posts/articles are present")


@then('articles should have titles and descriptions')
def step_verify_article_content(context):
    """Verify articles have titles and descriptions"""
    time.sleep(2)
    from selenium.webdriver.common.by import By
    headings = context.driver.find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4')
    paragraphs = context.driver.find_elements(By.TAG_NAME, 'p')

    assert len(headings) >= 1, "No article titles found"
    assert len(paragraphs) >= 1, "No article descriptions found"
    logger.info(f"✓ Found {len(headings)} titles and {len(paragraphs)} paragraphs")
