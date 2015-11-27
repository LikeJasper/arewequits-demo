@signup
Feature: Signup
    As someone interested in the website
    I want to sign up for an account
    So that I can use the website

    Scenario: Signup form submitted (normal case)

        Given I have not already signed up

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input valid signup details

        Then I will see the "confirm email" page
        And I will receive an email confirmation email

    Scenario: Signup form submitted when already added to a group

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input valid signup details

        Then I will see the "confirm email" page
        And I will receive an email confirmation email

    Scenario: Complete signup (normal case)

        Given I have not already signed up

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input valid signup details
        And I click on the verification link in the email confirm email

        Then I will see the "my groups" page
        And It will tell me to get started

    Scenario: Complete signup (invited user)

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input valid signup details
        And I click on the verification link in the email confirm email

        Then I will see the "login" page

    Scenario Outline: Attempted signup with obviously bad email

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input an invalid email ("<email>")
        And I input a valid "password"
        And I input a valid "first name"
        And I input a valid "last name"
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

        Examples: Obviously bad emails
            | email         |
            | NONE          |
            | amy           |
            | pass12345     |
            | @google.com   |
            | amybeech@     |

    Scenario Outline: Attempted signup with bad password (normal case)

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input an invalid password ("<password>")
        And I input a valid "first name"
        And I input a valid "last name"
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

        Examples: Bad passwords
            | password |
            | NONE     |
            | pass123  |

    Scenario Outline: Attempted signup with bad password (invited user)

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input an invalid password ("<password>")
        And I input a valid "first name"
        And I input a valid "last name"
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

        Examples: Bad passwords
            | password |
            | NONE     |
            | pass123  |

    Scenario: Attempted signup without first name (normal case)

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input an invalid first name
        And I input a valid "last name"
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup without first name (invited user)

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input an invalid first name
        And I input a valid "last name"
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup without last name (normal case)

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input a valid "first name"
        And I input an invalid last name
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup without last name (invited user)

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input a valid "first name"
        And I input an invalid last name
        And I check the terms of service box
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup without agreeing to terms of service (normal case)

        Given I am not logged in

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input a valid "first name"
        And I input a valid "last name"
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup without agreeing to terms of service (invited user)

        Given I have not already signed up
        But I have been added to a group

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input a valid "email"
        And I input a valid "password"
        And I input a valid "first name"
        And I input a valid "last name"
        And I press submit

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup with existing details

        Given I am not logged in
        But I have already signed up

        When I visit the "home" page
        And I click on the "Sign up button"
        And I input valid signup details

        Then I will see the signup form
        # And I will see an error message

    Scenario: Attempted signup when already logged in

        Given I have already signed up
        And I am logged in

        When I visit the "signup" page

        Then I will see the "my groups" page
