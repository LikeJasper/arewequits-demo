@login
Feature: Login
    As someone with an account
    I want to login to the website
    So that I can access my account

    Scenario Outline: Normal login when not in exactly 1 group

        Given I am not logged in
        But I have already signed up
        And I am a member of "<not_exactly_one>" group(s)

        When I visit the "home" page
        And I click on the "Log in button"
        And I input valid login details

        Then I will see the "my groups" page

        Examples: Numbers that are not one
            | not_exactly_one |
            | 0               |
            | 2               |

    Scenario: Normal login when in exactly 1 group

        Given I am not logged in
        But I have already signed up
        And I am a member of "1" group(s)

        When I visit the "home" page
        And I click on the "Log in button"
        And I input valid login details

        Then I will see the "view group" page

    Scenario Outline: Login with bad email address

        Given I am not logged in
        But I have already signed up

        When I visit the "home" page
        And I click on the "Log in button"
        And I input an invalid email ("<email>")
        And I input a valid "password"
        And I press submit

        Then I will see the login form
        # And I will see an error message

        Examples: Invalid login email addresses
            | email              |
            | NONE               |
            | amy                |
            | pass12345          |
            | @google.com        |
            | amybeech@          |
            | not@registered.com |

    Scenario Outline: Login with bad password

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Log in button"
        And I input a valid "email"
        And I input an invalid password ("<password>")
        And I press submit

        Then I will see the login form
        # And I will see an error message

        Examples: Bad passwords
            | password    |
            | NONE        |
            | pass123     |
            | notright123 |

    Scenario: Attempted login when already logged in

        Given I have already signed up
        And I am logged in

        When I visit the "login" page

        Then I will see the "my groups" page
