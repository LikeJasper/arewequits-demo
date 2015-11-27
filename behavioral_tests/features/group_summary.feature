@group_summary
Feature: Group summary
  
  As a user who is a member of a group
  I want to see a summary of the group totals for each member
  So that I can quickly see who is up/down and by how much

  Background: Standard pattern of members in and out of groups

    Given there are a number of signed up users in or out of various groups

  Scenario: View view group page

    Given I am logged in

    When I visit the "my groups" page
    And I click on the "Test group link"

    Then I will see the "view group" page
    And I will see the "members summary table"

  Scenario: Add first payment

    Given I am logged in

    When I visit the "add payment" page
    And I input valid payment details

    Then I will see the member balances have changed to incorporate the "new payment"

  Scenario: Add additional payment

    Given I am logged in
    And a number of payments have been created

    When I visit the "add payment" page
    And I input valid payment details

    Then I will see the member balances have changed to incorporate the "additional payment"

  Scenario: Edit payment

    Given I am logged in
    And a number of payments have been created

    When I visit the "edit payment" page
    And I input valid payment details

    Then I will see the member balances have changed to incorporate the "edited payment"

  Scenario: Delete payment

    Given I am logged in
    And a number of payments have been created

    When I visit the "edit payment" page
    And I click on the "enable delete button switch"
    And I click on the "delete button"

    Then I will see the member balances have changed to incorporate the "deleted payment"

  Scenario: Non-member visits view group page

    Given I am logged in

    When I visit the "view group" page for a group I am not a member of

    Then I will get a 404

  Scenario: Non-user visits view group page

    Given I am not logged in

    When I visit the "view group" page

    Then I will see the "landing" page