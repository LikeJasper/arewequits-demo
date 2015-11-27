@new_group
Feature: Create group
    As a user who wants to keep track of their expenses
    I want to create a group
    So that I can record payments for that group

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario: Create group form with no previous contacts

        Given I am a logged-in user with no existing contacts

        When I visit the "my groups" page
        And I click on the "Create new group button"

        Then I will see the "new group" page
        And I will see "no existing users" as options

    Scenario: Create group form with previous contacts

        Given I am logged in

        When I visit the "my groups" page
        And I click on the "Create new group button"

        Then I will see the "new group" page
        And I will see "my contacts" as options
        And I will see "no other users" as options

    @email
    Scenario: Successful group creation

        Given I am logged in

        When I visit the "new group" page
        And I input valid group details

        Then I will see the "view group" page
        And I will see the "group name" I gave when creating the group
        And I will see the "currency" I gave when creating the group
        And I will see the "members" I gave when creating the group
        And I will not see any users who were not given when creating the group
        And the added member will receive an email inviting them to sign up

    Scenario Outline: Attempted input of invalid create group details

        Given I am logged in

        When I visit the "new group" page
        And I put "<a valid detail>" in "<an input box>"
        And I put "<an invalid detail>" in "<an input box>"
        And I press submit

        Then I will see the "new group" page
        # And I will see an error message

        Examples: Invalid details for input boxes
            | a valid detail  | an input box | an invalid detail | an input box      |
            | valid@email.com | member email | NONE              | group name        |
            | Valid name      | group name   | NONE              | all member inputs |
            | Valid name      | group name   | amy               | member email      |
            | Valid name      | group name   | pass12345         | member email      |
            | Valid name      | group name   | @google.com       | member email      |
            | Valid name      | group name   | amybeech@         | member email      |

    Scenario: Non-user visits create group page

        Given I am not logged in

        When I visit the "new group" page

        Then I will see the "landing" page
