@game_service
Feature: Game Service

Background: Two Accounts
  When account service receives request for new account with details:
    | email          |
    | test@test.test |
  And account service receives request for new account with details:
    | email          |
    | test_one@test.test |
  Scenario: Create New Game
    When game service receives request to create new game with properties:
    | host_player    | invited_players |
    | test@test.test | test_one@test.test      |
    Then the game service successfully creates a new game
    When game service receives request for that game info
    Then the game service returns a game with info:
    | host_player    | invited_players    | game_status | pending_players |
    | test@test.test | test_one@test.test | pending     | test_one@test.test       |
