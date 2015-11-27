@edit_details
Feature: Edit details
    As someone who has signed up
    I want to edit my account details
    So that I can correct mistakes
    Or update my details to reflect changes

    Scenario: Successfully change name

        Given I have already signed up
        And I am logged in

        When I visit the "edit details" page
        And I input valid edit account details

        Then I will see the "account details" page
        And my new account details will be displayed

    Scenario: Change of email requires verification

        Given I have already signed up
        And I am logged in

        When I visit the "edit details" page
        And I input a valid "email"
        And I press submit

        Then I will see the "confirm email" page
        And I will receive an email confirmation email

    Scenario: Verify changed email

        Given I have already signed up
        And I am logged in

        When I visit the "edit details" page
        And I input a valid "email"
        And I press submit
        And I click on the verification link in the email confirm email

        Then I will see the "my groups" page
        And I will see the "email confirmed" message

    Scenario Outline: Attempted input of invalid account details

        Given I have already signed up
        And someone else has already signed up
        And I am logged in

        When I visit the "edit details" page
        And I put "<an invalid detail>" in "<an input box>"
        And I press submit

        Then I will see the "edit details" page
        # And I will see an error message

        Examples: Invalid details for input boxes
            | an invalid detail  | an input box |
            | NONE               | first name   |
            | NONE               | last name    |
            | NONE               | email        |
            | amy                | email        |
            | pass12345          | email        |
            | @google.com        | email        |
            | amybeech@          | email        |
            | monica@friends.com | email        |

    Scenario: Non-user visits edit details page

        Given I am not logged in

        When I visit the "edit details" page

        Then I will see the "landing" page
