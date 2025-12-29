@regression @industries
Feature: Industries Page Functionality
  As a potential client
  I want to view the industries Faberwork serves
  So that I can see if they have expertise in my industry

  Background:
    Given I am on the Faberwork homepage
    When I click on the "Industries" menu

  @industries @page_load
  Scenario: Industries page loads successfully
    Then the Industries page should load successfully
    And the page title should be "Industries We Serve"

  @industries @content
  Scenario: All industry sectors are listed
    Then I should see the following industries:
      | Industry Name                  |
      | Energy                         |
      | Finance                        |
      | Private Equity & Hedge Funds   |
      | Healthcare                     |
      | Insurance                      |
      | Retail                         |
      | Startup                        |
      | Telecom                        |
      | Transportation                 |

  @industries @filter
  Scenario: Industry filter functionality exists
    Then the filter form should be present
    And the filter dropdown should be accessible

  @industries @search
  Scenario: Search functionality is available
    When I click on the search button
    Then the search field should be visible
    And I should be able to enter search terms

  @industries @consultation_form
  Scenario: Consultation form is accessible on Industries page
    When I scroll to the consultation form
    Then the consultation form should be visible
    And all required form fields should be present

  @industries @newsletter
  Scenario: Newsletter signup is available
    When I scroll to the newsletter section
    Then the newsletter email field should be visible
    And the newsletter submit button should be clickable

  @industries @navigation
  Scenario: Navigation elements work on Industries page
    Then all navigation links should be present
    And the Faberwork logo should be visible
    When I click on the logo
    Then I should be redirected to the homepage
