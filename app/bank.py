from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from app.init_db import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Float, CheckConstraint("balance>=0"), default=0.0)

    def __init__(self, session, name, balance=0):
        self.name = name
        self.balance = balance
        self.session = session
        self.session.add(self)
        self.session.commit()

    def __str__(self):
        return (f"Account of {self.name}")
    
    def deposit(self, amount):
        if not isinstance(amount, int | float):
            raise TypeError("Integer of float expected")
        if amount <= 0:
            raise ValueError("Positive deposit amount expected")
        self.balance += amount
        Transaction(self.session, "deposit", amount, self)
        self.session.commit()

    def withdraw(self, amount):
        if not isinstance(amount, int | float):
            raise TypeError("Integer or float expected")
        if amount <= 0 or self.balance < amount:
            raise ValueError("Positive withdraw amount expected / positive balance after withdraw expected")
        self.balance -= amount
        Transaction(self.session, "withdraw", amount, self)
        self.session.commit()

    def initiate_transfer(self, amount, other):
        if not isinstance(amount, int | float):
            raise TypeError("Integer or float expected")
        if amount <= 0 or self.balance < amount:
            raise ValueError("Positive amount expected / positive balance after transfer expected")
        Transaction(self.session, "transfer", amount, self, other)
        
    def confirm_transfer(self, type, amount, transaction):
        if not isinstance(transaction, Transaction):
            raise KeyError("Confirmed transaction required to confirm transfer")
        if type == "send":
            self.balance -= amount
        elif type == "receive":
            self.balance += amount
        self.session.commit()

    def get_balance(self):
        return self.balance
    
    # @hybrid_property
    # def balance(self):
    #     return self._balance
    
    # @balance.setter
    # def balance(self, value):
    #     if not isinstance(value, int | float) or value < 0:
    #         raise ValueError("Positive balance expected")
    #     self._balance = value


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, CheckConstraint("amount>0"), nullable=False)
    DateTime = Column(DateTime, default=datetime.now)
    initiator_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"))

    def __init__(self, session, type, amount, initiator_account, receiver_account=None):

        if not isinstance(amount, int | float) or amount <= 0:
            raise ValueError("Postive amount expected")
        if not isinstance(initiator_account, Account):
            raise KeyError("registered initiator account required for transaction")
        
        if type == "withdraw" or type == "transfer":
            if initiator_account.get_balance() < amount:
                raise ValueError("Balance of sender account inferior to amount")
        
        self.type = type
        self.amount = amount
        self.initiator = initiator_account
        self.initiator_account_id = self.initiator.id

        if type == "transfer":
            if not isinstance(receiver_account, Account):
                raise KeyError("Registered receiver account required for transaction") 
            self.receiver = receiver_account
            self.receiver_account_id = self.receiver.id
            self.initiator.confirm_transfer("send", amount, self)
            self.receiver.confirm_transfer("receive", amount, self)

        session.add(self)
        session.commit()

    def __str__(self):
        return (f"Transaction {self.id} of {self.amount}, from {self.sender} to {self.receiver}")