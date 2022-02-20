from yoyo import step

steps = [
    step('''
        CREATE TABLE transaction_history (id INT PRIMARY KEY AUTO_INCREMENT, 
        user_id INT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        amount DECIMAL(15,2), balance DECIMAL(15,2), purpose TEXT, FOREIGN KEY 
        (user_id) REFERENCES users_balance (user_id) ON DELETE CASCADE);
        ''')]
