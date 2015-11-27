@delete_group
Feature: Delete group
    As a user who is a member of a group
    I want to delete the group
    So that I can forget about it
    Or make a new group from scratch if I made a huge mistake

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario: Successfully delete group

        Given I am logged in

        When I visit the "edit group" page
        And I click on the "delete tab"
        And I click on the "enable delete button switch"
        And I click on the "delete button"

        Then I will see the "my groups" page
        And I will not see the group I deleted

    Scenario: Attempted delete group without enabling button

        Given I am logged in

        When I visit the "edit group" page
        And I click on the "delete tab"
        And I click on the "delete button"

        Then I will see the "edit group" page
