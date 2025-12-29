@regression @success_stories
Feature: Success Stories Page Functionality
  As a potential client
  I want to view Faberwork's success stories and case studies
  So that I can understand their track record and capabilities

  Background:
    Given I am on the Faberwork homepage
    When I click on the "Success Stories" menu

  @success_stories @page_load
  Scenario: Success Stories page loads successfully
    Then the Success Stories page should load successfully
    And the page title should be "Customer Success Stories"

  @success_stories @case_studies
  Scenario: Case study cards are displayed
    Then I should see multiple case study cards
    And each card should have a title
    And each card should have a description
    And each card should have a "Read More" link

  @success_stories @filter
  Scenario: Filter functionality works for success stories
    Then the filter form should be present
    When I select a filter option
    Then the page should filter the results accordingly

  @success_stories @filter_categories
  Scenario: Filter dropdown contains industry and tech stack options
    When I click on the filter dropdown
    Then I should see industry filter options
    And I should see technology stack filter options
    And I should see options like "AI", "Snowflake", "Healthcare", "Energy"

  @success_stories @search
  Scenario: Search functionality is available for stories
    When I click on the search button
    Then the search field should appear
    And I can search for specific case studies
    And search results should be displayed dynamically

  @success_stories @read_more
  Scenario: Read More links work on case study cards
    When I click on a "Read More" link on a case study card
    Then I should be taken to the full case study or expanded content

  @success_stories @chatbot
  Scenario: Chatbot is accessible on Success Stories page
    When I click on the chatbot button
    Then the chatbot dialog should open
    And I should see the chat input field
    And I should be able to send a message

  @success_stories @navigation
  Scenario: Navigation works properly on Success Stories page
    Then all navigation links should be present
    And clicking any navigation link should work correctly
