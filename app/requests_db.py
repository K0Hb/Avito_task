import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('HOST')
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
TABLE_CREATE = [
    'CREATE TABLE users_balance (user_id INT PRIMARY KEY UNIQUE, balance '
    'DECIMAL(15,2));',
    'CREATE TABLE transaction_history (id INT PRIMARY KEY AUTO_INCREMENT, '
    'user_id INT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, transaction TEXT, '
    'balance DECIMAL(15,2), purpose TEXT, FOREIGN KEY (user_id)  '
    'REFERENCES users_balance (user_id) ON DELETE CASCADE);',
]

connection = pymysql.connect(host=HOST,
                             user=USER_DB,
                             password=PASSWORD,
                             database=DB_NAME,
                             cursorclass=pymysql.cursors.DictCursor)


def create_user(user_id, connection=connection):
    '''
    Функция создает пользователся в БД
    '''
    with connection.cursor() as cursor:
        connection.ping()
        result = cursor.execute(f"INSERT INTO users_balance (user_id) "
                                f"VALUES ('{user_id}');")
        connection.commit()
        connection.close()
        return result


def delete_user(user_id, connection=connection):
    '''
    Функция удаляет пользователся из БД.
    '''
    with connection.cursor() as cursor:
        connection.ping()
        result = cursor.execute(f"DELETE FROM users_balance "
                                f"WHERE user_id = '{user_id}';")
        connection.commit()
        connection.close()
        return result


def get_user_info(user_id, connection=connection):
    '''
    Функция выдает информацию о  пользователе из БД.
    '''
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM users_balance "
                       f"WHERE user_id = {user_id};")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if result == ():
            result = None
        return result


def enrollment_and_write_downs(user_id, balance, connection=connection):
    '''
        Функция изменяет состояние баланса пользователя в БД.
        balance - значение баланса после транзакци
    '''
    if balance < 0:
        raise Exception('Баланс не может быть ниже 0.')
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"UPDATE users_balance SET balance = '{balance}'"
                       f" WHERE user_id = '{user_id}'")
        connection.commit()
        connection.close()


def add_history_user(user_id, number, balance, purpose, connection=connection):
    '''
    Функция добавляет историю транзакции в БД.
    number - сумма транзакции
    balance - значение баланса после транзакци
    '''
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(
            f"INSERT INTO transaction_history "
            f"(user_id, transaction, balance, purpose) "
            f"VALUES ('{user_id}', '{number}', '{balance}', '{purpose}');")
        connection.commit()
        connection.close()


def get_history_user(user_id, sorted_amount=False, sorted_data=False,
                     connection=connection):
    '''
    Функция выдает историй пользователя транзакции в БД.
    sorted_data - сортировка по датам
    sorted_amount - сортировка по сумме транзакций
    '''
    with connection.cursor() as cursor:
        connection.ping()
        if sorted_amount:
            cursor.execute(
                f"SELECT data, balance, transaction, purpose "
                f"FROM transaction_history "
                f"WHERE user_id = {user_id} ORDER BY transaction;")
        elif sorted_data:
            cursor.execute(
                f"SELECT data, balance, transaction, purpose "
                f"FROM transaction_history "
                f"WHERE user_id = {user_id} ORDER BY data;")
        else:
            cursor.execute(
                f"SELECT data, balance, transaction, purpose "
                f"FROM transaction_history WHERE user_id = {user_id};")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if result == ():
            return None
        return result
