import pytest

from app.bank import Account
import tests.parameters as parameters


@pytest.mark.database
@pytest.mark.parametrize(parameters.valid_account[0], parameters.valid_account[1])
def test_create_valid_account(session_function, account_factory, name, initial_balance):
    account = account_factory(session_function, name, initial_balance)
    assert account.name == name
    assert account.balance == initial_balance
    assert session_function.commit.call_count == 1 # 1 commit for the account created

@pytest.mark.module_session
@pytest.mark.database
@pytest.mark.parametrize(parameters.multiple_valid_account[0], parameters.multiple_valid_account[1])
def test_create_multiple_valid_account(session_module, account_factory, name, expected_num_accounts):
    account = account_factory(session_module, name)
    assert account.name == name
    assert len(session_module.query(Account).all()) == expected_num_accounts
    assert session_module.commit.call_count == expected_num_accounts # 1, 2 and 3 commit for the 3 account created

@pytest.mark.module_session
@pytest.mark.database
def test_create_another_account(session_module, account_factory):
    account_factory(session_module, "L")
    assert len(session_module.query(Account).all()) == 4
    assert session_module.commit.call_count == 4 # 4 commit for the 3 account created previously and the new one

@pytest.mark.skip(reason="WIP, le filter ne fonctionne pas et retourne tout les account au lieu d'un")
@pytest.mark.module_session
@pytest.mark.database
def test_delete_account(session_module):
    account = session_module.query(Account).filter(Account.name == "L").one()
    session_module.delete(account)
    session_module.commit()
    assert len(session_module.query(Account).all()) == 3