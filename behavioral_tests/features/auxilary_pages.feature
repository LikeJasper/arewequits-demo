@aux_pages
Feature: Auxilary pages
    As a robot
    Or as a person interested in the site metadata
    I want to access the relevant file(s)
    So that I can perform analysis etc

    Scenario: robots.txt

        Given I am a robot

        When I visit the "robots" page

        Then I will see the "robots" page

    Scenario: humans.txt

        Given I am interested in the humans

        When I visit the "humans" page

        Then I will see the "humans" page
