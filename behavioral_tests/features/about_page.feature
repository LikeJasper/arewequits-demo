@about
Feature: About page
    As someone interested in the website
    I want to find out more information about it
    So that I can decide whether to sign up
    Or I can get a better idea of how to use the service

    Scenario: Non-user trying to find out more

        Given I am not logged in

        When I visit the "home" page
        And I click on the "about page link"

        Then I will see the "about" page

    Scenario: Logged-in user trying to get more help

        Given I have already signed up
        And I am logged in

        When I visit the "home" page
        And I click on the "about page link"

        Then I will see the "about" page
