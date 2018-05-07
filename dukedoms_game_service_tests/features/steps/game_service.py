from behave import given, then, when
from hamcrest import assert_that, equal_to, contains_inanyorder, is_in, has_item
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

@when('game service receives request to create new game with properties')
def step_create_game(context):
    """
    Create a new game with game service
    """
    for row in context.table:
        host_player = row['host_player']

        results, status = context.clients.game_service.gameCreation.create_new_game(
            newGameRequest={
                'hostPlayer': host_player,
                'hostPlayerId': context.account_ids[host_player],
                'invitedPlayers': row['invited_players'].split(',')
            }
        ).result()

        assert_that(status.status_code, equal_to(200))
        context.status_code = status.status_code
        context.game_id = results.game_id


@then('the game service successfully creates a new game')
def assert_game_created(context):
    assert_that(context.status_code, equal_to(200))

@then('game service returns an id')
@when('game service receives request for that game info')
def step_request_game_info(context):
    pass

@then('the game service returns a game with info')
def assert_game_info(context):
    results, status = context.clients.game_service.gameInfo.get_game_info(
        gameId=context.game_id
    ).result()

    assert_that(results.players['hostPlayer'], equal_to(context.table.rows[0]['host_player']))

    for player in context.table.rows[0]['invited_players'].split(','):
        assert_that(player, is_in(results.players['invitedPlayers']))
