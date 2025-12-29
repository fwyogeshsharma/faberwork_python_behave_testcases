@regression @contact
Feature: Contact Us Page Functionality
  As a potential client
  I want to contact Faberwork
  So that I can inquire about their services

  Background:
    Given I am on the Faberwork homepage
    When I click on the "Contact" menu

  @contact @page_load
  Scenario: Contact Us page loads successfully
    Then the Contact page should load successfully
    And the page heading should be "Get in Touch With Us"

  @contact @office_info
  Scenario: USA office contact information is displayed
    Then I should see USA office phone number "+1-410-884-9169"
    And I should see email address "info@faberwork.com"
    And I should see USA office address "10045 Red Run Blvd Suite 250, Owings Mills, MD 21117"

  @contact @office_info
  Scenario: India office contact information is displayed
    Then I should see India office phone number "+91-74140-82984"
    And I should see email address "info@faberwork.com"
    And I should see India office address containing "Metropolis Tower, Ajmer Road, Jaipur"

  @contact @map
  Scenario: Office location maps are displayed
    Then I should see a map for the USA office location
    And I should see a map for the India office location
    And the maps should be clickable to open in Google Maps

  @contact @form
  Scenario: Contact form has all required fields
    When I view the consultation form
    Then the form should have a name field
    And the form should have a company field
    And the form should have an email field
    And the form should have a phone field
    And the form should have a message textarea
    And the form should have a submit button

  @contact @form_validation @positive
  Scenario: Submit contact form with valid data
    When I fill in the contact form with:
      | Field   | Value                              |
      | Name    | John Smith                         |
      | Company | ABC Corporation                    |
      | Email   | john.smith@abccorp.com            |
      | Phone   | +1-555-123-4567                   |
      | Message | I would like to discuss a project |
    And I submit the contact form
    Then I should see a success message

  @contact @form_validation @negative
  Scenario: Submit contact form with invalid email
    When I fill in the contact form with:
      | Field   | Value           |
      | Name    | Test User       |
      | Email   | invalid-email   |
    And I submit the contact form
    Then I should see an error message about invalid email

  @contact @social_media
  Scenario: Social media links are present
    Then I should see a LinkedIn link
    And the LinkedIn link should point to Faberwork's company page

  @contact @newsletter
  Scenario: Newsletter subscription is available
    When I scroll to the newsletter section
    Then the newsletter email field should be visible
    And I can subscribe to the newsletter

  @contact @navigation
  Scenario: Navigation elements work on Contact page
    Then all navigation links should be present
    And the Faberwork logo should be visible
    And footer elements should be displayed
