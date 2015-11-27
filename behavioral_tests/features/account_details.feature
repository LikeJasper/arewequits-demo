@account_details
Feature: Account details
    As someone who has signed up
    I want to view my account details
    So that I can check they are right
    Or confirm what information is held about me

    Scenario: Logged in user checks account details

        Given I have already signed up
        And I am logged in

        When I visit the "account details" page

        Then I will see the "first name" I gave when I signed up
        And I will see the "last name" I gave when I signed up
        And I will see the "email" I gave when I signed up

    Scenario: Non-member visits account details page

        Given I am not logged in

        When I visit the "account details" page

        Then I will see the "landing" page
