@delete_payment
Feature: Delete payment
    As a user who is a member of a group with existing payments
    I want to delete a payment
    So that I can discard it if it shouldn't be counted after all
    Or make a new payment from scratch if I made a huge mistake

    Background: Standard pattern of members in and out of groups with payments

        Given there are a number of signed up users in or out of various groups
        And a number of payments have been created

    Scenario: View delete payment form

        Given I am logged in

        When I visit the "view group" page
        And I click on the "first payment row"
        And I click on the "edit payment icon"

        Then I will see the "edit payment" page
        And I will see the "delete button"

    Scenario: Successfully delete payment

        Given I am logged in

        When I visit the "edit payment" page
        And I click on the "enable delete button switch"
        And I click on the "delete button"

        Then I will see the "view group" page
        And I will not see the payment I deleted

    Scenario: Attempted delete payment without enabling button

        Given I am logged in

        When I visit the "edit payment" page
        And I click on the "delete button"

        Then I will see the "edit payment" page
