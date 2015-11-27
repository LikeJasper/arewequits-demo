@my_groups
Feature: My groups
    As someone who has signed up
    I want to view my groups
    So that I can see an overview of my group balances
    And I can create new groups

    Scenario: No groups

        Given I have already signed up
        And I am logged in

        When I visit the "my groups" page

        Then I will not see the group summary table
        And I will see the get started card for "groups"

    Scenario: First group created

        Given I have already signed up
        And I am logged in

        When I visit the "new group" page
        And I input valid group details
        And I visit the "my groups" page

        Then I will see the "group summary table"
        And the group summary table will show my group name "New group"
        And the group summary table will not show any other groups
        And the group summary table will show an empty balance for my new group

    Scenario: Additional group created

        Given there are a number of signed up users in or out of various groups
        And I am logged in

        When I visit the "new group" page
        And I input valid group details
        And I visit the "my groups" page

        Then I will see the "group summary table"
        And the group summary table will show my group name "New group"
        And the group summary table will show my other groups
        And the group summary table will show an empty balance for my new group

    Scenario: Payments added to groups

        Given there are a number of signed up users in or out of various groups
        And I am logged in

        When I visit the "add payment" page
        And I input valid payment details
        And I visit the "my groups" page

        Then I will see the "group summary table"
        And the group summary table will show an updated balance for my group
        And the group summary table will show an unchanged balance for each other group

    Scenario: Non-user visits add members page

        Given I am not logged in

        When I visit the "my groups" page

        Then I will see the "landing" page
