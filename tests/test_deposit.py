import pytest

from app.bank import Account, Transaction
import tests.parameters as parameters


@pytest.mark.database
@pytest.mark.parametrize(parameters.valid_deposit[0], parameters.valid_deposit[1])
def test_valid_deposit(session_function, account_factory, name, initial_balance, amount):
    account = account_factory(session_function, name, initial_balance)
    account.deposit(amount)
    transaction = session_function.query(Transaction).first()
    assert account.balance == initial_balance + amount
    assert len(session_function.query(Transaction).all()) == 1
    assert transaction.type == "deposit"
    assert transaction.datetime != "Null"
    assert session_function.commit.call_count == 3 # 3 commit for the account created, deposit and transaction created

@pytest.mark.database
def test_invalid_type_deposit(session_function, account_factory):
    account = account_factory(session_function, "Q", 100)
    with pytest.raises(TypeError):
        account.deposit("100$")
    assert account.balance == 100
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created

@pytest.mark.database
@pytest.mark.parametrize(parameters.invalid_deposit[0], parameters.invalid_deposit[1])
def test_invalid_amount_deposit(session_function, account_factory, name, initial_balance, amount):
    account = account_factory(session_function, name, initial_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)
    assert account.balance == initial_balance
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created