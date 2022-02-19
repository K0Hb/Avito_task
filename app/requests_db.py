import os
import pymysql
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
        try:
            result = cursor.execute("INSERT INTO users_balance (user_id) VALUES (%(user_id)s);""", {'user_id': user_id})
        except Exception:
            return 0
        connection.commit()
        connection.close()
        return result



def delete_user(user_id, connection=connection):
    '''
    Функция удаляет пользователся из БД.
    '''
    with connection.cursor() as cursor:
        connection.ping()
        result = cursor.execute("""DELETE FROM users_balance WHERE user_id = '%(user_id)s'""", {'user_id': user_id})
        connection.commit()
        connection.close()
        return result


def get_user_info(user_id, connection=connection):
    '''
    Функция выдает информацию о  пользователе из БД.
    '''
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute('''SELECT * FROM users_balance WHERE user_id = %(user_id)s''', {'user_id': user_id})
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
        cursor.execute("""UPDATE users_balance SET balance = '%(balance)s' WHERE user_id = '%(user_id)s'""", {'user_id': user_id, 'balance' : balance})
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
        cursor.execute("""
            INSERT INTO transaction_history 
            (user_id, amount, balance, purpose) 
            VALUES ('%(user_id)s', '%(number)s', '%(balance)s', %(purpose)s)""",
            {'user_id': user_id, 'balance' : balance, 'number' : number, 'purpose': purpose})
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
            cursor.execute("""
                SELECT data, balance, amount, purpose 
                FROM transaction_history 
                WHERE user_id = %(user_id)s ORDER BY transaction""",
                 {'user_id': user_id})
        elif sorted_data:
            cursor.execute("""
                SELECT data, balance, amount, purpose 
                FROM transaction_history 
                WHERE user_id = %(user_id)s ORDER BY data""",
                {'user_id': user_id})
        else:
            cursor.execute("""
                SELECT data, balance, amount, purpose 
                FROM transaction_history WHERE user_id = %(user_id)s""",
                {'user_id': user_id})
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if result == ():
            return None
        return result