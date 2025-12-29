@regression @carousel
Feature: Carousel and Slider Functionality
  As a user
  I want to interact with carousels and sliders
  So that I can view success stories and testimonials

  Background:
    Given I am on the Faberwork homepage

  @carousel @success_stories
  Scenario: Success stories carousel navigation
    When I scroll to the success stories section
    Then the success stories carousel should be visible
    And carousel navigation buttons should be present

  @carousel @next
  Scenario: Navigate carousel using next button
    Given the success stories carousel is visible
    When I click the carousel next button
    Then the next carousel item should be displayed
    And the carousel should animate smoothly

  @carousel @previous
  Scenario: Navigate carousel using previous button
    Given the success stories carousel is visible
    And I am on the second carousel item
    When I click the carousel previous button
    Then the previous carousel item should be displayed

  @carousel @autoplay
  Scenario: Carousel auto-rotates
    Given the success stories carousel is visible
    When I wait for 5 seconds
    Then the carousel should automatically advance to the next item

  @carousel @testimonials
  Scenario: Testimonial slider displays correctly
    When I scroll to the testimonials section
    Then the testimonial slider should be visible
    And testimonial quotes should be displayed
    And testimonials should rotate automatically

  @carousel @indicators
  Scenario: Carousel indicators work
    Given the success stories carousel is visible
    When I click on carousel indicator 3
    Then carousel item 3 should be displayed
    And the indicator should be highlighted

  @carousel @touch_swipe
  Scenario: Carousel responds to touch/swipe gestures
    Given I am viewing the carousel on a mobile device
    When I swipe left on the carousel
    Then the next carousel item should appear

  @carousel @keyboard
  Scenario: Carousel keyboard navigation
    Given the success stories carousel has focus
    When I press the right arrow key
    Then the next carousel item should be displayed
    When I press the left arrow key
    Then the previous carousel item should be displayed

  @carousel @count
  Scenario: Verify number of carousel items
    Given the success stories carousel is visible
    Then there should be at least 10 carousel items
    And each item should have content

  @carousel @pause_on_hover
  Scenario: Carousel pauses on hover
    Given the carousel is auto-rotating
    When I hover over the carousel
    Then the carousel should pause auto-rotation
    When I move the mouse away
    Then the carousel should resume auto-rotation
