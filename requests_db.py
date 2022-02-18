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
        cursor.execute(f"INSERT INTO users_balance (user_id) VALUES ('{user_id}');")
        connection.commit()
        connection.close()


def get_user_info(user_id, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM users_balance WHERE user_id = {user_id};")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result


def enrollment_and_write_downs(user_id, number, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"UPDATE users_balance SET balance = '{number}' WHERE user_id = '{user_id}'")
        connection.commit()
        connection.close()


def add_history_user(user_id, transaction, balance, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"INSERT INTO transaction_history (user_id, transaction, balance) VALUES ('{user_id}', '{transaction}', '{balance}');")
        connection.commit()
        connection.close()


def get_history_user(user_id, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM transaction_history WHERE user_id = {user_id};")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result

# print(get_user_info(2,True))
# print(enrollment_and_write_downs(2, 400))
# print(get_user_info(2,True))

# CREATE DATABASE Avito;
# CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL, patronymic VARCHAR(255) NOT NULL);
# CREATE TABLE balance (id INT PRIMARY KEY AUTO_INCREMENT, balance NUMERIC, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));
# CREATE TABLE users_balance (user_id INT PRIMARY KEY UNIQUE ,  balance DECIMAL(15,2));
# CREATE TABLE transaction_history (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, transaction TEXT, balance DECIMAL(15,2), FOREIGN KEY (user_id)  REFERENCES users_balance (user_id));