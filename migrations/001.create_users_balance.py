from yoyo import step

steps = [
    step('''CREATE TABLE users_balance (user_id INT PRIMARY KEY UNIQUE, 
    balance DECIMAL(15,2));'''
         )
]
