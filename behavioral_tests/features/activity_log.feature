@activity_log
Feature: Activity log
    As a user who is a member of a group
    I want to see when people make changes
    So that I can see if someone is changing things they shouldn't
    Or work out whether a legitimate change has already been made

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario: Check when group was created

        Given I am logged in

        When I visit the "view group" page
        And I click on the "activity log button"

        Then I will see when "the group was created"
        And I will see who "created the group"

    Scenario: Add a payment

        Given I am logged in

        When I visit the "add payment" page
        And I input valid payment details
        And I click on the "activity log button"

        Then I will see when "the payment was created"
        And I will see who "created the payment"

        When I click on the "payment link"

        Then I will see the "description" I gave when "creating" the payment

    Scenario: Edit a payment

        Given a number of payments have been created
        And I am logged in

        When I visit the "edit payment" page
        And I input valid payment details
        And I click on the "activity log button"

        Then I will see when "the payment was edited"
        And I will see who "edited the payment"

        When I click on the "payment link"

        Then I will see the "description" I gave when "editing" the payment

    Scenario: Delete a payment

        Given a number of payments have been created
        And I am logged in

        When I visit the "edit payment" page
        And I click on the "enable delete button switch"
        And I click on the "delete button"
        And I click on the "activity log button"

        Then I will see when "the payment was deleted"
        And I will see who "deleted the payment"

    @now
    Scenario: Restore a payment

        Given a number of payments have been created
        And I am logged in

        When I visit the "edit payment" page
        And I click on the "enable delete button switch"
        And I click on the "delete button"
        And I visit the "edit payment" page
        And I click on the "restore payment button"
        And I click on the "activity log button"

        Then I will see when "the payment was restored"
        And I will see who "restored the payment"

    Scenario Outline: Add existing user from another group

        Given I am logged in

        When I go to "<an add members form>"
        And I select an existing user from another group
        And I press submit
        And I click on the "activity log button"

        Then I will see when "the user was added to the group"
        And I will see who "added the user to the group"

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario Outline: Add existing user not from another group

        Given I am logged in

        When I go to "<an add members form>"
        And I enter the email address of "an existing user"
        And I press submit
        And I click on the "activity log button"

        Then I will see when "the user was added to the group"
        And I will see who "added the user to the group"

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario Outline: Add non-user

        Given I am logged in

        When I go to "<an add members form>"
        And I enter the email address of "a non-user"
        And I press submit
        And I click on the "activity log button"

        Then I will see when "the user was added to the group"
        And I will see who "added the user to the group"

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario: Non-member visits add members page

        Given I am logged in

        When I visit the "activity log" page for a group I am not a member of

        Then I will get a 404

    Scenario: Non-user visits add members page

        Given I am not logged in

        When I visit the "activity log" page

        Then I will see the "landing" page
