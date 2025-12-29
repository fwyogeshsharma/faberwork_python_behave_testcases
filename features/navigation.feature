@regression @navigation
Feature: Website Navigation
  As a user
  I want to navigate through different pages
  So that I can access information and services

  Background:
    Given I am on the Faberwork homepage

  @navigation @menu
  Scenario Outline: Navigate to different pages via menu
    When I click on the "<menu_item>" menu
    Then I should be on the "<expected_page>" page
    And the URL should contain "<url_fragment>"

    Examples:
      | menu_item       | expected_page | url_fragment |
      | Services        | Services      | services     |
      | Industries      | Industries    | industries   |
      | Success Stories | Success       | success      |
      | About Us        | About         | about        |
      | Contact Us      | Contact       | contact      |

  @navigation @logo
  Scenario: Logo click returns to homepage
    Given I am on the Services page
    When I click on the logo
    Then I should be on the homepage
    And the homepage should load successfully

  @navigation @footer
  Scenario: Footer links are functional
    Given I am on the homepage
    When I scroll to the footer
    Then footer links should be present
    And footer links should be clickable

  @navigation @breadcrumb
  Scenario: Breadcrumb navigation works
    Given I am on a service details page
    When I look at the breadcrumb
    Then it should show the navigation path
    And I should be able to click breadcrumb links

  @navigation @backbutton
  Scenario: Browser back button works
    Given I am on the homepage
    When I navigate to the Services page
    And I click the browser back button
    Then I should be back on the homepage
