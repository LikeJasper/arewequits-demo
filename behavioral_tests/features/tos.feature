@tos
Feature: Terms of service
    As someone concerned about the law
    I want to read the terms of service
    So that I know what I'm agreeing to

    Scenario: Non-user interested in terms

        Given I am not logged in

        When I visit the "home" page
        And I click on the "tos link"

        Then I will see the "tos" modal

    Scenario: Logged-in user looking for confirmation

        Given I have already signed up
        And I am logged in

        When I visit the "home" page
        And I click on the "tos link"

        Then I will see the "tos" modal
