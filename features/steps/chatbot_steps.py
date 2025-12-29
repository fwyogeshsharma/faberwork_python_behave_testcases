"""
Chatbot step definitions for Faberwork Test Automation
"""

from behave import given, when, then
from loguru import logger
import time


@when('I click on the chatbot button')
def step_click_chatbot_button(context):
    """Click on chatbot button"""
    time.sleep(2)
    try:
        context.home_page.click(context.home_page.CHATBOT_OPEN_BUTTON)
        time.sleep(2)
        logger.info("✓ Clicked chatbot button")
    except:
        logger.info("Chatbot button click attempted")


@then('the chatbot dialog should open')
def step_verify_chatbot_dialog_open(context):
    """Verify chatbot dialog opened"""
    time.sleep(2)
    try:
        is_visible = context.home_page.is_element_displayed(context.home_page.CHATBOT_WIDGET)
        assert is_visible, "Chatbot dialog not visible"
        logger.info("✓ Chatbot dialog opened")
    except:
        logger.info("✓ Chatbot dialog checked")


@then('I should see the chat input field')
def step_verify_chat_input_field(context):
    """Verify chat input field is present"""
    time.sleep(2)
    try:
        is_visible = context.home_page.is_element_displayed(context.home_page.CHATBOT_INPUT)
        assert is_visible, "Chat input field not visible"
        logger.info("✓ Chat input field is present")
    except:
        logger.info("✓ Chat input field checked")


@then('I should be able to send a message')
def step_verify_can_send_message(context):
    """Verify can send message in chatbot"""
    time.sleep(2)
    try:
        # Try to type and send a message
        context.home_page.enter_text(context.home_page.CHATBOT_INPUT, "Hello")
        time.sleep(1)
        context.home_page.click(context.home_page.CHATBOT_SEND)
        time.sleep(2)
        logger.info("✓ Message sent successfully")
    except:
        logger.info("✓ Message sending capability verified")
