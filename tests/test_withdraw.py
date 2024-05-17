import pytest

from app.bank import Account, Transaction
import tests.parameters as parameters


@pytest.mark.database
@pytest.mark.parametrize(parameters.valid_withdraw[0], parameters.valid_withdraw[1])
def test_valid_withdraw(session_function, account_factory, name, initial_balance, amount):
    account = account_factory(session_function, name, initial_balance)
    account.withdraw(amount)
    transaction = session_function.query(Transaction).first()
    assert account.balance == initial_balance - amount
    assert len(session_function.query(Transaction).all()) == 1
    assert transaction.type == "withdraw"
    assert transaction.datetime != "Null"
    assert session_function.commit.call_count == 3 # 3 commit for the account created, withdraw and transaction created

@pytest.mark.database
def test_invalid_type_withdraw(session_function, account_factory):
    account = account_factory(session_function, "Q", 100)
    with pytest.raises(TypeError):
        account.withdraw("100$")
    assert account.balance == 100
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created

@pytest.mark.database
@pytest.mark.parametrize(parameters.invalid_withdraw[0], parameters.invalid_withdraw[1])
def test_invalid_amount_withdraw(session_function, account_factory, name, initial_balance, amount):
    account = account_factory(session_function, name, initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)
    assert account.balance == initial_balance
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created

@pytest.mark.database
@pytest.mark.parametrize(parameters.insufficient_fund_withdraw[0], parameters.insufficient_fund_withdraw[1])
def test_insufficient_fund_withdraw(session_function, account_factory, name, initial_balance, amount):
    account = account_factory(session_function, name, initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)
    assert account.balance == initial_balance
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created