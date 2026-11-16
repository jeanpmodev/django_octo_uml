Feature: Interactive UML Entity Architecture Visualizer
  As a Django developer or system administrator
  I want to inspect and export the project's entity-relationship diagram from the admin panel
  So that I can visualize database models and relationships in real time

  Background:
    Given an authenticated superuser exists

  Scenario: Render UML diagram excluding Django core apps by default
    When the user navigates to the UML Entity Diagram dashboard
    Then the response status code should be 200
    And the page should contain a valid Graphviz DOT payload
    And Django core auth models should be hidden by default

  Scenario: Render UML diagram including Django core apps
    When the user navigates to the UML Entity Diagram dashboard with core apps enabled
    Then the response status code should be 200
    And the DOT payload should include the "User" model

  Scenario: Download raw Graphviz DOT file
    When the user requests the DOT file download
    Then the response should return a downloadable ".dot" file

