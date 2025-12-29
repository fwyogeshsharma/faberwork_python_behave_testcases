@regression @search
Feature: Search Functionality
  As a user
  I want to search for content on the website
  So that I can quickly find relevant information

  Background:
    Given I am on the Faberwork homepage

  @search @positive
  Scenario Outline: Search for content with valid keywords
    When I search for "<keyword>"
    Then search results should be displayed
    And results should be relevant to "<keyword>"

    Examples:
      | keyword              |
      | software development |
      | mobile app           |
      | AI solutions         |
      | database             |
      | testing              |

  @search @empty
  Scenario: Search with empty query
    When I submit an empty search query
    Then I should see a message indicating empty search

  @search @no_results
  Scenario: Search with no matching results
    When I search for "xyzabc123nonexistent"
    Then I should see a "no results found" message
    And suggestions for alternative searches may be shown

  @search @autocomplete
  Scenario: Search autocomplete suggestions
    When I start typing "soft" in the search field
    Then autocomplete suggestions should appear
    And suggestions should include "software"

  @search @filter
  Scenario: Filter search results
    Given I have performed a search for "development"
    When I apply a filter for "articles"
    Then only article results should be displayed

  @search @special_characters
  Scenario: Search handles special characters
    When I search for "C++ & Python"
    Then the search should handle special characters correctly
    And relevant results should be displayed

  @search @case_insensitive
  Scenario: Search is case-insensitive
    When I search for "SOFTWARE"
    And I search for "software"
    Then both searches should return the same results

  @search @pagination
  Scenario: Search results pagination
    Given I have performed a search with many results
    When I view the search results
    Then results should be paginated
    And I should be able to navigate to page 2

  @search @clear
  Scenario: Clear search query
    Given I have entered a search query
    When I click the clear search button
    Then the search field should be empty
    And search results should be cleared

  @search @recent
  Scenario: Recent searches display
    Given I have performed multiple searches
    When I click on the search field
    Then my recent searches should be displayed
    And I should be able to click on a recent search
