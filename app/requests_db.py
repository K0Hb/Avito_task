import pymysql
import os
from dotenv import load_dotenv


load_dotenv()
HOST = os.getenv('HOST')
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')

connection = pymysql.connect(host=HOST,
                             user=USER_DB,
                             password=PASSWORD,
                             database=DB_NAME,
                             cursorclass=pymysql.cursors.DictCursor)


def create_user(user_id, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        result = cursor.execute(f"INSERT INTO users_balance (user_id) VALUES ('{user_id}');")
        connection.commit()
        connection.close()
        return result

def delete_user(user_id, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        result = cursor.execute(f"DELETE FROM users_balance WHERE user_id = '{user_id}';")
        connection.commit()
        connection.close()
        return result


def get_user_info(user_id, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM users_balance WHERE user_id = {user_id};")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if result == ():
            result = None
        return result


def enrollment_and_write_downs(user_id, number, connection=connection):
    if number < 0:
        raise Exception('Баланс не может быть ниже 0.')
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"UPDATE users_balance SET balance = '{number}' WHERE user_id = '{user_id}'")
        connection.commit()
        connection.close()


def add_history_user(user_id, transaction, balance, purpose,connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"INSERT INTO transaction_history (user_id, transaction, balance, purpose) VALUES ('{user_id}', '{transaction}', '{balance}', '{purpose}');")
        connection.commit()
        connection.close()


def get_history_user(user_id, sorted_amount=False, sorted_data=False, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        if sorted_amount == False and sorted_data == False:
            cursor.execute(f"SELECT data, balance, transaction, purpose FROM transaction_history WHERE user_id = {user_id};")
        elif sorted_amount:
            cursor.execute(f"SELECT data, balance, transaction, purpose FROM transaction_history WHERE user_id = {user_id} ORDER BY transaction;")
        elif sorted_data:
            cursor.execute(f"SELECT data, balance, transaction, purpose FROM transaction_history WHERE user_id = {user_id} ORDER BY data;")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if result == ():
            return None
        return result

# print(get_user_info(2,True))
# print(enrollment_and_write_downs(2, 400))
# print(get_user_info(2,True))
# create_user(2999)
# delete_user(2999)
# print(delete_user(2999))

# CREATE DATABASE Avito;
# CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL, patronymic VARCHAR(255) NOT NULL);
# CREATE TABLE balance (id INT PRIMARY KEY AUTO_INCREMENT, balance NUMERIC, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));
# CREATE TABLE users_balance (user_id INT PRIMARY KEY UNIQUE ,  balance DECIMAL(15,2));
# CREATE TABLE transaction_history (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
# transaction TEXT, balance DECIMAL(15,2), purpose TEXT, FOREIGN KEY (user_id)  REFERENCES users_balance (user_id) ON DELETE CASCADE);

# print(create_user(35))
# print(delete_user(33))

# create_user(2999)
# enrollment_and_write_downs(2999, 100.5)
# add_history_user(2999, 100.5, 100.5, 'test1')
# enrollment_and_write_downs(2999, 50.05)
# add_history_user(2999, 50.05, 155.55, 'test2')
# print(get_history_user(2999))
# delete_user(2999)