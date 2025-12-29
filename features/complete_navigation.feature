@regression @navigation @full
Feature: Complete Website Navigation
  As a website visitor
  I want to navigate through all pages of the Faberwork website
  So that I can access all information and services

  Background:
    Given I am on the Faberwork homepage

  @navigation @menu
  Scenario Outline: Navigate to all main pages from homepage
    When I click on the "<menu_item>" menu
    Then I should be on the "<page_name>" page
    And the page should load successfully

    Examples:
      | menu_item        | page_name          |
      | Services         | Services           |
      | Industries       | Industries         |
      | Success Stories  | Success Stories    |
      | Latest Thinking  | Latest Thinking    |
      | About us         | About Us           |
      | Contact          | Contact Us         |

  @navigation @logo
  Scenario: Logo navigation returns to homepage from any page
    When I click on the "Services" menu
    And I click on the Faberwork logo
    Then I should be on the homepage
    And the homepage should load successfully

  @navigation @footer
  Scenario: Footer links are present and accessible on all pages
    Then footer links are present
    When I click on the "Services" menu
    Then footer links are present
    When I click on the "About us" menu
    Then footer links are present

  @navigation @breadcrumb
  Scenario: Navigation through multiple pages works correctly
    When I click on the "Services" menu
    Then I should be on the "Services" page
    When I click on the "Industries" menu
    Then I should be on the "Industries" page
    When I click on the "Success Stories" menu
    Then I should be on the "Success Stories" page
    When I click on the "Latest Thinking" menu
    Then I should be on the "Latest Thinking" page

  @navigation @contact_from_pages
  Scenario: Contact page is accessible from any page
    When I click on the "Services" menu
    And I click on the "Contact" menu
    Then I should be on the "Contact Us" page
    And the contact form should be visible

  @navigation @consistent
  Scenario: Navigation menu is consistent across all pages
    Then all navigation links should be present
    When I click on the "Services" menu
    Then all navigation links should be present
    When I click on the "About us" menu
    Then all navigation links should be present
    When I click on the "Contact" menu
    Then all navigation links should be present
