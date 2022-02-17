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


def get_user(id=None, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        try:
            cursor.execute(f"SELECT * FROM users_balance WHERE user_id = {id};")
            result = cursor.fetchall()
            connection.commit()
            if result:
                return result
            else:
                return 'Такого пользователя нет'
        except Exception as e:
            print(e)
        finally:
            connection.close()

print(get_user(3))
# print(create_user(4))

# CREATE DATABASE Avito;
# CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL, patronymic VARCHAR(255) NOT NULL);
# CREATE TABLE balance (id INT PRIMARY KEY AUTO_INCREMENT, balance NUMERIC, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));
# CREATE TABLE users_balance (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT UNIQUE ,  balance NUMERIC, history JSON);