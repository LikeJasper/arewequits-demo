@edit_group
Feature: Edit group
    As a user who is a member of a group
    I want to edit the group details
    So that I can correct mistakes
    Or update group details to reflect changes

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario: Successfully edit group name

        Given I am logged in

        When I visit the "edit group" page
        And I input a valid "edited group name"
        And I press submit

        Then I will see the "view group" page
        And I will see the "edited group name" I gave when editing the group

    Scenario: Successfully change group currency

        Given I am logged in

        When I visit the "edit group" page
        And I select a new currency
        And I press submit

        Then I will see the "view group" page
        And I will see the "currency" I gave when editing the group

    Scenario: Attempted submission without a group name

        Given I am logged in

        When I visit the "edit group" page
        And I clear the "edited group name"
        And I press submit

        Then I will see the "view group" page
        And I will see the original "group name"

    Scenario: Non-member visits edit group page

        Given I am logged in

        When I visit the "edit group" page for a group I am not a member of

        Then I will get a 404

    Scenario: Non-user visits edit group page

        Given I am not logged in

        When I visit the "edit group" page

        Then I will see the "landing" page
