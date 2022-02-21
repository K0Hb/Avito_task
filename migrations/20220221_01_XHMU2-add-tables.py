"""
Add tables
"""

from yoyo import step

__depends__ = {'001.init'}

steps = [
    step('''CREATE TABLE users_balance (user_id INT PRIMARY KEY UNIQUE, 
    balance DECIMAL(15,2));'''), step('''
        CREATE TABLE transaction_history (id INT PRIMARY KEY AUTO_INCREMENT, 
        user_id INT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        amount DECIMAL(15,2), balance DECIMAL(15,2), purpose TEXT, FOREIGN KEY 
        (user_id) REFERENCES users_balance (user_id) ON DELETE CASCADE);
        '''),
]
