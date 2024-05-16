from bank import Account
from init_db import init_session

def main():

    session = init_session()

    # Create accounts
    account1 = Account(session, "Q")
    account2 = Account(session, "L")

    # Make deposits
    account1.deposit(100)
    account2.deposit(50)
    
    # Make withdraws
    account1.withdraw(5)
    account2.withdraw(10)

    # Make transfer
    account1.initiate_transfer(50, account2)

    session.close()
	
if __name__ == "__main__":
	main()