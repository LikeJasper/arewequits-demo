@help
Feature: Help button
  
  As someone finding it difficult to use AreWeQuits?
  I want to have access to helpful information
  So that I can find out how to do the things I want to do

  Background: Standard pattern of members in and out of groups with payments

    Given there are a number of signed up users in or out of various groups
    And a number of payments have been created
    And I am logged in

  Scenario Outline: Show help message

    When I visit the "<page>" page
    And I click on the "help button"

    Then I should see the help message(s)

    Examples: Pages with help messages
      | page         |  
      | my groups    |  
      | view group   |  
      | add payment  |  
      | edit payment |  

  Scenario Outline: Hide help message

    When I visit the "<page>" page
    And I click on the "help button"
    And I click on the "help button"

    Then I should not see the help message(s)

    Examples: Pages with help messages
      | page         |  
      | my groups    |  
      | view group   |  
      | add payment  |  
      | edit payment |  
  