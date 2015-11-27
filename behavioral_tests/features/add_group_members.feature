@add_members
Feature: Add members to group
    As a user who is a member of an existing group
    I want to add new members to the group
    So I can enter payments which involve them too

    Background: Standard pattern of members in and out of groups

        Given there are a number of signed up users in or out of various groups

    Scenario Outline: Add existing user from another group

        Given I am logged in

        When I go to "<an add members form>"
        And I select an existing user from another group
        And I press submit

        Then I will see the "view group" page
        And I will see the added member's "name"
        And I will see the member's balance is "0.00"

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario Outline: Add existing user not from another group

        Given I am logged in

        When I go to "<an add members form>"
        And I enter the email address of "an existing user"
        And I press submit

        Then I will see the "view group" page
        And I will see the added member's "name"
        And I will see the member's balance is "0.00"

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    @email
    Scenario Outline: Add non-user

        Given I am logged in

        When I go to "<an add members form>"
        And I enter the email address of "a non-user"
        And I press submit

        Then I will see the "view group" page
        And I will see the added member's "email"
        And I will see the member's balance is "0.00"
        And the added member will receive an email inviting them to sign up

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario Outline: Attempted submission of empty form

        Given I am logged in

        When I go to "<an add members form>"
        And I press submit

        Then I will see the "add members" page
        # And I will see an error message

        Examples: Add members form locations
            | an add members form                        |
            | the add members page                       |
            | the add members tab of the edit group page |

    Scenario Outline: Attempted input of invalid emails

        Given I am logged in

        When I go to "<an add members form>"
        And I input an invalid email ("<email>")
        And I press submit

        Then I will see the "<add members form page>" page
        # And I will see an error message

        Examples: Add members form locations and bad emails
            | an add members form                        | email         | add members form page |
            | the add members page                       | NONE          | add members           |
            | the add members page                       | amy           | add members           |
            | the add members page                       | pass12345     | add members           |
            | the add members page                       | @google.com   | add members           |
            | the add members page                       | amybeech@     | add members           |
            | the add members tab of the edit group page | NONE          | add members           |
            | the add members tab of the edit group page | amy           | edit group            |
            | the add members tab of the edit group page | pass12345     | edit group            |
            | the add members tab of the edit group page | @google.com   | edit group            |
            | the add members tab of the edit group page | amybeech@     | edit group            |

    Scenario: Non-member visits add members page

        Given I am logged in

        When I visit the "add members" page for a group I am not a member of

        Then I will get a 404

    Scenario: Non-user visits add members page

        Given I am not logged in

        When I visit the "add members" page

        Then I will see the "landing" page
