@regression @forms
Feature: Form Submissions and Validations
  As a potential client
  I want to submit consultation and contact forms
  So that I can get in touch with Faberwork

  Background:
    Given I am on the Faberwork homepage

  @forms @consultation @positive
  Scenario: Submit consultation form with valid data
    When I fill in the consultation form with valid data:
      | Field   | Value                    |
      | Name    | John Doe                 |
      | Company | Tech Innovations Inc     |
      | Email   | john.doe@techinno.com    |
      | Phone   | +1-555-123-4567          |
      | Message | I need help with my project |
    And I submit the consultation form
    Then I should see a success message
    And the success message should contain "thank you" or "received"

  @forms @consultation @negative
  Scenario Outline: Consultation form validation for invalid email
    When I enter "<email>" in the email field
    And I submit the consultation form
    Then I should see a validation error
    And the error should indicate invalid email format

    Examples:
      | email               |
      | invalid             |
      | @example.com        |
      | test@               |
      | test..email@ex.com  |
      | test email@ex.com   |

  @forms @consultation @required
  Scenario: Consultation form requires mandatory fields
    When I submit the consultation form without filling any fields
    Then I should see validation errors for required fields
    And the form should not be submitted

  @forms @consultation @phone
  Scenario Outline: Phone number validation
    When I enter "<phone>" in the phone field
    And I submit the consultation form
    Then the phone field should "<result>"

    Examples:
      | phone           | result         |
      | +1-555-123-4567 | accept         |
      | 5551234567      | accept         |
      | (555) 123-4567  | accept         |
      | invalid         | show error     |
      | 123             | show error     |

  @forms @contact @positive
  Scenario: Submit contact form successfully
    Given I am on the Contact page
    When I fill in the contact form with:
      | Field   | Value                                  |
      | Name    | Jane Smith                             |
      | Email   | jane.smith@example.com                 |
      | Phone   | +1-555-987-6543                        |
      | Company | Global Solutions Ltd                   |
      | Subject | Inquiry about services                 |
      | Message | I would like to know more about your services |
    And I submit the contact form
    Then I should see a success message
    And the message should confirm submission

  @forms @contact @negative
  Scenario: Contact form with missing required fields
    Given I am on the Contact page
    When I enter only email "test@example.com"
    And I submit the contact form
    Then I should see errors for missing fields
    And the Name field should show an error
    And the Message field should show an error

  @forms @newsletter @positive
  Scenario: Subscribe to newsletter with valid email
    When I enter a valid email in the newsletter field
    And I click the newsletter subscribe button
    Then I should see a newsletter subscription confirmation

  @forms @newsletter @negative
  Scenario Outline: Newsletter subscription with invalid email
    When I enter "<email>" in the newsletter field
    And I click the newsletter subscribe button
    Then I should see a newsletter error message

    Examples:
      | email            |
      | invalid          |
      | @domain.com      |
      | test@            |

  @forms @autofill
  Scenario: Form fields support auto-fill
    Given I am on the homepage
    When I click on the name field
    Then the name field should support auto-fill
    And the email field should support auto-fill

  @forms @character_limit
  Scenario: Message field respects character limits
    Given I am on the Contact page
    When I enter 5000 characters in the message field
    Then the field should either accept all characters or show a limit warning

  @forms @special_characters
  Scenario: Forms handle special characters correctly
    When I fill in the consultation form with special characters:
      | Field   | Value                          |
      | Name    | O'Brien-Smith                  |
      | Company | Müller & Söhne GmbH            |
      | Message | Testing special chars: <>&"'   |
    And I submit the consultation form
    Then the form should handle the data correctly
    And no JavaScript errors should occur
