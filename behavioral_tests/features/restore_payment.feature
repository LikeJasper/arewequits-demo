@restore_payment
Feature: Restore payment

  As a user who is a member of a group with deleted payments
  I want to restore a payment
  So that I can include it if it should be counted after all
  Or avoid making a new payment from scratch if it was deleted by mistake

  Background: Standard pattern of members in and out of groups with payments

    Given there are a number of signed up users in or out of various groups
    And a number of payments have been created
    And I am logged in

  Scenario: Deleted payment shows restore option

    When I visit the "edit payment" page
    And I click on the "enable delete button switch"
    And I click on the "delete button"
    And I visit the "edit payment" page

    Then I will see the "restore payment button"

  Scenario: Successfully restore payment

    When I visit the "edit payment" page
    And I click on the "enable delete button switch"
    And I click on the "delete button"
    And I visit the "edit payment" page
    And I click on the "restore payment button"

    Then I will see the "view group" page
    And I will see the payment I restored

  Scenario: Active payment doesn't show restore option

    When I visit the "edit payment" page

    Then I will not see the "restore payment button"