@regression @services
Feature: Services Page Functionality
  As a potential client
  I want to view Faberwork's service offerings
  So that I can understand their capabilities

  Background:
    Given I am on the Faberwork homepage
    When I click on the "Services" menu

  @services @page_load
  Scenario: Services page loads successfully
    Then the Services page should load successfully
    And the page title should contain "Services"
    And all service offerings are visible on the page

  @services @content
  Scenario: Verify all 8 service offerings are present
    Then I should see the following services:
      | Service Name                        |
      | SnowPro® Certified Developers      |
      | Cost Effective AI Implementation    |
      | Mobile App Development             |
      | Software Development               |
      | ERP Solutions                      |
      | Database Solutions                 |
      | Software Re-engineering            |
      | Test Automation                    |

  @services @sections
  Scenario: Verify key sections are present on Services page
    Then I should see the "Trusted by Leading Technology Companies" section
    And I should see the "What Sets Us Apart" section
    And I should see the "Let's Work Together" section

  @services @cta
  Scenario: Verify CTA buttons are functional
    Then the "START NOW" button should be visible
    And the "START NOW" button should be clickable
    And the "Get Started" button should be visible

  @services @contact_info
  Scenario: Verify contact information is displayed
    Then the USA phone number "+1-410-884-9169" should be visible
    And the India phone number "+91-74140-82984" should be visible
    And the phone numbers should be clickable

  @services @consultation_form
  Scenario: Consultation form is accessible on Services page
    When I scroll to the consultation form
    Then the consultation form should be visible
    And the form should have name, company, email, and phone fields

  @services @navigation
  Scenario: Navigation menu is present on Services page
    Then all navigation links should be present
    And the Faberwork logo should be visible
