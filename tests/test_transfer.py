import pytest

from app.bank import Account, Transaction
import tests.parameters as parameters


@pytest.mark.database
@pytest.mark.parametrize(parameters.valid_transfer[0], parameters.valid_transfer[1])
def test_valid_transfer(session_function, account_factory, initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount):
    initiator_account = account_factory(session_function, initiator_name, initiator_initial_balance)
    receiver_account = account_factory(session_function, receiver_name, receiver_initial_balance)
    initiator_account.initiate_transfer(receiver_account, amount)
    transaction = session_function.query(Transaction).first()
    assert initiator_account.balance == initiator_initial_balance - amount
    assert receiver_account.balance == receiver_initial_balance + amount
    assert len(session_function.query(Transaction).all()) == 1
    assert transaction.type == "transfer"
    assert transaction.datetime != "Null"
    assert session_function.commit.call_count == 5 # 5 commit for the two account created, the transaction and the two confirm transfer

@pytest.mark.database
def test_invalid_type_transfer(session_function, account_factory):
    initiator_account = account_factory(session_function, "Q", 100)
    receiver_account = account_factory(session_function, "L", 0)
    with pytest.raises(TypeError):
        initiator_account.initiate_transfer(receiver_account, "100$")
    assert initiator_account.balance == 100
    assert receiver_account.balance == 0
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 2 # 2 commit for the two account created

@pytest.mark.database
def test_invalid_receiver_transfer(session_function, account_factory):
    initiator_account = account_factory(session_function, "Q", 100)
    receiver_account = "L"
    with pytest.raises(KeyError):
        initiator_account.initiate_transfer(receiver_account, 100)
    assert initiator_account.balance == 100
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 1 # 1 commit for the account created

@pytest.mark.database
@pytest.mark.parametrize(parameters.invalid_transfer[0], parameters.invalid_transfer[1])
def test_invalid_transfer(session_function, account_factory, initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount):
    initiator_account = account_factory(session_function, initiator_name, initiator_initial_balance)
    receiver_account = account_factory(session_function, receiver_name, receiver_initial_balance)
    with pytest.raises(ValueError):
        initiator_account.initiate_transfer(receiver_account, amount)
    assert initiator_account.balance == initiator_initial_balance
    assert receiver_account.balance == receiver_initial_balance
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 2 # 2 commit for the two account created

@pytest.mark.database
@pytest.mark.parametrize(parameters.insufficient_fund_transfer[0], parameters.insufficient_fund_transfer[1])
def test_insufficient_fund_transfer(session_function, account_factory, initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount):
    initiator_account = account_factory(session_function, initiator_name, initiator_initial_balance)
    receiver_account = account_factory(session_function, receiver_name, receiver_initial_balance)
    with pytest.raises(ValueError):
        initiator_account.initiate_transfer(receiver_account, amount)
    assert initiator_account.balance == initiator_initial_balance
    assert receiver_account.balance == receiver_initial_balance
    assert len(session_function.query(Transaction).all()) == 0
    assert session_function.commit.call_count == 2 # 2 commit for the two account created
