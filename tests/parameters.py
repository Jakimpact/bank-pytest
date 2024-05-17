valid_account = (
    "name, initial_balance",
    [("Q", 100000), ("Doe", 0), ("John Doe", 500.56)]   
)

multiple_valid_account = (
    "name, expected_num_accounts",
    [("Q", 1), ("Doe", 2), ("John Doe", 3)]   
)

valid_deposit = (
    "name, initial_balance, amount",
    [("Q", 100000, 25000), ("Doe", 0, 5), ("John Doe", 500.56, 0.04)]
)

invalid_deposit = (
    "name, initial_balance, amount",
    [("Q", 100000, -25000), ("Doe", 0, 0), ("John Doe", 500.56, -0.04)]    
)

valid_withdraw = (
    "name, initial_balance, amount",
    [("Q", 100000, 25000), ("Doe", 5, 5), ("John Doe", 500.56, 0.04)]
)

invalid_withdraw = (
    "name, initial_balance, amount",
    [("Q", 100000, -25000), ("Doe", 0, 0), ("John Doe", 500.56, -0.04)]    
)

insufficient_fund_withdraw = (
    "name, initial_balance, amount",
    [("Q", 100000, 250000), ("Doe", 0, 5), ("John Doe", 500.56, 500.57)] 
)

valid_transfer = (
    "initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount",
    [
        ("Q", 100000, "L", 50000, 25000),
        ("Doe", 5, "L", 0, 5),
        ("John Doe", 500.56, "L", 200.07, 0.04)
    ]
)

invalid_transfer = (
    "initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount",
    [
        ("Q", 100000, "L", 50000, -25000),
        ("Doe", 0, "L", 0, 0),
        ("John Doe", 500.56, "L", 200.07, -0.04)
    ]
)

insufficient_fund_transfer = (
    "initiator_name, initiator_initial_balance, receiver_name, receiver_initial_balance, amount",
    [
        ("Q", 100000, "L", 50000, 250000),
        ("Doe", 0, "L", 0, 5),
        ("John Doe", 500.56, "L", 200.07, 500.57)
    ]
)