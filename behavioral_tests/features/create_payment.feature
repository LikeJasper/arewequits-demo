@new_payment
Feature: Create payment

    As a user who is a member of a group
    I want to create a payment
    So that I can record an expense
    And find out how much everybody owes

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario: View create payment form

        Given I am logged in

        When I visit the "view group" page
        And I click on the "Add new payment button"

        Then I will see the "add payment" page
        And I will see "the group members" as options

    Scenario: Successful payment creation

        Given I am logged in

        When I visit the "add payment" page
        And I input valid payment details

        Then I will see the "view group" page
        And I will see the "icon" I gave when "creating" the payment
        And I will see the "date" I gave when "creating" the payment
        And I will see the "amount" I gave when "creating" the payment
        And I will see the "description" I gave when "creating" the payment
        And I will see the "payer" I gave when "creating" the payment
        And I will see the "receivers" I gave when "creating" the payment

    Scenario: Successful payment creation without description

        Given I am logged in

        When I visit the "add payment" page
        And I put "24.00" in "amount"
        And I put "NONE" in "description"
        And I press submit

        Then I will see the "view group" page
        And I will see the "amount" I gave when "creating" the payment

    Scenario Outline: Attempted input of invalid create payment details

        Given I am logged in

        When I visit the "add payment" page
        And I put "24.00" in "amount"
        And I put "Test payment" in "description"
        And I put "<an invalid detail>" in "<an input box>"
        And I press submit

        Then I will see the "add payment" page
        # And I will see an error message

        Examples: Invalid details for input boxes
            | an invalid detail | an input box |
            | NONE              | amount       |
            | twenty four       | amount       |
            | 24.24.24          | amount       |
            | NONE              | who_for      |

    Scenario: Non-member visits create payment page

        Given I am logged in

        When I visit the "add payment" page for a group I am not a member of

        Then I will get a 404

    Scenario: Non-user visits create payment page

        Given I am not logged in

        When I visit the "add payment" page

        Then I will see the "landing" page
