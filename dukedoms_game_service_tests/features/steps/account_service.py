from behave import given, when
from hamcrest import assert_that, equal_to, is_not
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

@given('an empty account database')
def clear_account_service_db(context):
    """
    drop any existing information from tables for a clean test run.
    """
    engine = create_engine(context.env_urls.account_service_db)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    session.execute('TRUNCATE TABLE accounts')
    session.commit()
    session.close()

@when('account service receives request for new account with details')
def step_new_account(context):
    """
    attempt to create a new account
    """
    for row in context.table:
        account_email = row['email']
        account_request = context.clients.account_service.get_model('NewAccountRequest')(
            email=account_email
        )

        result, status = context.clients.account_service.newAccount.create_new_account(
            newAccountRequest=account_request
        ).result()

        assert_that(status.status_code, equal_to(200))
        assert_that(result.account_id, is_not(None))

        context.account_ids[account_email] = result.account_id
