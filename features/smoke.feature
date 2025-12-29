@smoke @critical
Feature: Smoke Tests for Faberwork Website
  As a QA engineer
  I want to run smoke tests
  So that I can verify critical functionality is working

  Background:
    Given the Faberwork website is accessible

  @smoke @homepage
  Scenario: Homepage loads successfully
    When I navigate to the homepage
    Then the homepage should load successfully
    And the logo should be visible
    And all navigation links should be present

  @smoke @navigation
  Scenario: Main navigation menu works
    Given I am on the homepage
    When I click on the "Services" menu
    Then I should be on the Services page
    And the page should load successfully

  @smoke @form
  Scenario: Consultation form is accessible
    Given I am on the homepage
    When I scroll to the consultation form
    Then the consultation form is visible
    And all required form fields are present

  @smoke @contact
  Scenario: Contact page is accessible
    Given I am on the homepage
    When I click on the "Contact Us" menu
    Then I should be on the Contact page
    And the contact form is visible
