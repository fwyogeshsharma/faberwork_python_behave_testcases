@regression @about
Feature: About Us Page Functionality
  As a potential client or visitor
  I want to learn about Faberwork's company and team
  So that I can understand their background and expertise

  Background:
    Given I am on the Faberwork homepage
    When I click on the "About us" menu

  @about @page_load
  Scenario: About Us page loads successfully
    Then the About page should load successfully
    And the page title should be "Who We Are"
    And I should see "Established 2003" text

  @about @company_info
  Scenario: Company overview information is displayed
    Then I should see company overview information
    And I should see "Snowflake Partner Network" mentioned
    And I should see "enterprise applications" mentioned

  @about @leadership_team
  Scenario: All leadership team members are displayed
    Then I should see the following team members:
      | Name              | Title                        |
      | Alok Pancholi     | Founder & CEO                |
      | Yogesh Sharma     | SVP, Delivery                |
      | Jaideep Singh     | Senior Director, Delivery    |
      | Ram Singh         | Senior Technical Lead        |
      | Saurabh Jain      | Senior Technical Lead        |
      | Vikas Sharma      | Senior Technical Lead        |

  @about @team_photos
  Scenario: Team member photos are displayed
    Then I should see profile photos for team members
    And the photo for "Alok Pancholi" should be visible
    And the photo for "Yogesh Sharma" should be visible

  @about @read_more
  Scenario: Read more functionality works for team bios
    When I click on a "Read more" button for team bio
    Then the full bio content should be expanded
    And the button should change to "Read less"

  @about @cta
  Scenario: Call-to-action section is present
    When I scroll to the bottom of the page
    Then I should see "Let's Work Together" section
    And the "START NOW" button should be visible

  @about @navigation
  Scenario: Navigation elements are present on About page
    Then all navigation links should be present
    And the Faberwork logo should be visible
    And the footer should be visible
