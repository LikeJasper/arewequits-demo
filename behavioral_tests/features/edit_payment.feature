@edit_payment
Feature: Edit payment
    As a user who is a member of a group
    I want to edit a payment
    So that I can correct a mistake
    And find out how much everybody owes

    Background: Standard pattern of members in and out of groups with payments

        Given there are a number of signed up users in or out of various groups
        And a number of payments have been created

    Scenario: View edit payment form

        Given I am logged in

        When I visit the "view group" page
        And I click on the "first payment row"
        And I click on the "edit payment icon"

        Then I will see the "edit payment" page
        And I will see "the group members" as options

    Scenario: Successful payment edit

        Given I am logged in

        When I visit the "edit payment" page
        And I input valid payment details

        Then I will see the "view group" page
        And I will see the "icon" I gave when "editing" the payment
        And I will see the "date" I gave when "editing" the payment
        And I will see the "amount" I gave when "editing" the payment
        And I will see the "description" I gave when "editing" the payment
        And I will see the "payer" I gave when "editing" the payment
        And I will see the "receivers" I gave when "editing" the payment

    Scenario Outline: Attempted input of invalid edit payment details

        Given I am logged in

        When I visit the "edit payment" page
        And I put "24.00" in "amount"
        And I put "Test payment" in "description"
        And I put "<an invalid detail>" in "<an input box>"
        And I press submit

        Then I will see the "edit payment" page
        # And I will see an error message

        Examples: Invalid details for input boxes
            | an invalid detail | an input box |
            | NONE              | amount       |
            | twenty four       | amount       |
            | 24.24.24          | amount       |
            | NONE              | who_for      |

    Scenario: Non-member visits edit payment page

        Given I am logged in

        When I visit the "edit payment" page for a group I am not a member of

        Then I will get a 404

    Scenario: Non-user visits edit payment page

        Given I am not logged in

        When I visit the "edit payment" page

        Then I will see the "landing" page
