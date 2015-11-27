@logout
Feature: Logout
    As someone logged into the website
    I want to log out
    So that other people can't access my details
    Or someone else can log in using the same browser

    Scenario Outline: Logged in user logs out

        Given I have already signed up
        And I am logged in

        When I visit the "<relevant_page>" page
        And I click on the "menu icon"
        And I click on the "Log out"

        Then I will see the "landing" page

        Examples: Pages you can log out from
            | relevant_page   |
            | my groups       |
            | new group       |
            | account details |
            | edit details    |
            | about           |

    Scenario: Attempted log out when not logged in

        Given I am not logged in

        When I visit the "logout" page

        Then I will see the "landing" page
