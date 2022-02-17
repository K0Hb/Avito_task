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


def create_user(user_id, balance=None, history=None, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        try:
            cursor.execute(f"INSERT INTO users_balance (user_id) VALUES ('{user_id}');")
            connection.commit()
            return 'Пользователь успешно создан'
        except pymysql.err.IntegrityError as e:
            return 'Такой пользователь уже существует'
        finally:
            connection.close()


def get_user_info(id=None,all=False, balance=False, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        try:
            if all:
                cursor.execute(f"SELECT * FROM users_balance WHERE user_id = {id};")
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return result
                else:
                    return 'Такого пользователя нет'
            elif balance:
                cursor.execute(f"SELECT balance FROM users_balance WHERE user_id = {id};")
                result = cursor.fetchall()
                connection.commit()
                if result[0]['balance'] is not None:
                    return result
                else:
                    return 'Счет не сформирован'
        except Exception as e:
            print(e)
            return e
        finally:
            connection.close()


def enrollment_and_write_downs(user_id, sum):
    with connection.cursor() as cursor:
        connection.ping()
        try:
            cursor.execute(f"UPDATE users_balance SET balance = '{sum}' WHERE user_id = '{user_id}'")
            connection.commit()
            return 'Баланс успешно пополнен'
        except Exception as e:
            return e
        finally:
            connection.close()



print(enrollment_and_write_downs(3, 100))
# print(create_user(4))

# CREATE DATABASE Avito;
# CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL, patronymic VARCHAR(255) NOT NULL);
# CREATE TABLE balance (id INT PRIMARY KEY AUTO_INCREMENT, balance NUMERIC, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));
# CREATE TABLE users_balance (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT UNIQUE ,  balance NUMERIC, history JSON);