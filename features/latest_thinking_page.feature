@regression @latest_thinking
Feature: Latest Thinking Page Functionality
  As a visitor interested in technology trends
  I want to read Faberwork's blog and articles
  So that I can learn about their expertise and insights

  Background:
    Given I am on the Faberwork homepage
    When I click on the "Latest Thinking" menu

  @latest_thinking @page_load
  Scenario: Latest Thinking page loads successfully
    Then the Latest Thinking page should load successfully
    And the page title should be "Latest Thinking"
    And I should see the subtitle "Notes and Trends"

  @latest_thinking @articles
  Scenario: Article cards are displayed
    Then I should see multiple article cards
    And each article card should have a featured image
    And each article card should have a title
    And each article card should have a description
    And each article card should have a "Read More" button

  @latest_thinking @search
  Scenario: Article search functionality works
    When I click on the search button
    Then the search input field should appear
    When I enter "AI" in the search field
    Then I should see search results for "AI"
    And the results should be displayed in a dropdown

  @latest_thinking @filter
  Scenario: Category filter works for articles
    Then the filter form should be present
    When I select a category from the filter dropdown
    Then the articles should be filtered by the selected category

  @latest_thinking @categories
  Scenario Outline: Filter dropdown contains multiple category options
    When I click on the filter dropdown
    Then I should see the category "<category>"

    Examples:
      | category                |
      | AI                      |
      | Agentic AI              |
      | Automation              |
      | Business                |
      | Data                    |
      | Healthcare              |
      | IoT                     |
      | Machine Learning        |
      | Snowflake               |
      | Software Development    |

  @latest_thinking @read_article
  Scenario: Clicking on article title opens the article
    When I click on an article title
    Then I should be navigated to the article page or expanded view

  @latest_thinking @search_debounce
  Scenario: Search has debounce functionality
    When I type quickly in the search field
    Then the search should wait before making requests
    And results should appear after a short delay

  @latest_thinking @consultation_modal
  Scenario: Consultation modal can be opened from Latest Thinking page
    When I click on "Get Started" or consultation button
    Then the consultation modal should open
    And the modal should have a contact form

  @latest_thinking @navigation
  Scenario: All navigation elements work on Latest Thinking page
    Then all navigation links should be present
    And the logo should be clickable
    And footer links should be accessible
