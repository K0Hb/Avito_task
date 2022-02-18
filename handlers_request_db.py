from requests_db import *


def handler_create_user(user_id):
    try:
        create_user(user_id)
        return f'Пользователь c id {user_id} успешно создан'
    except pymysql.err.IntegrityError as e:
        return f'Пользователь c id {user_id} уже существует'


def handler_user_info(user_id, all=False, balance=False,):
    try:
        if all:
            user_info = get_user_info(user_id, all=all, balance=balance)
            if user_info:
                return user_info
            else:
                return f'Пользователь с id {user_id}, не создан'
        elif balance:
            user_balance = get_user_info(user_id, balance=balance)[0]['balance']
            if user_balance:
                return float(user_balance)
            else:
                return f'У пользователя с id {user_id}, не сформирован счет'
    except Exception as e:
            return f'При запросе произошла ошибка: {e}'


def handler_transactions(user_id, number, enrollment=False, write_down=False):
    try:
        balance = handler_user_info(user_id, balance=True)
        if enrollment:
            new_balance = balance + float(number)
            enrollment_and_write_downs(user_id, new_balance)
            return f'Успешно пополнен баланс пользователя с id {user_id}, на сумму({number})'
        elif write_down:
            if balance - number <0:
                return f'У пользователся с id {user_id} недостаточно средств на балансе, для списания суммы'
            else:
                new_balance = balance - float(number)
                enrollment_and_write_downs(user_id, new_balance)
                return f'У пользователя с id {user_id} успешно списана сумма({number}) с баланса'
    except Exception as e:
        return f'При транзакции произошла ошибка: {e}'

# print(handler_transactions(2, 600.25, enrollment=True))
# print(handler_user_info(2, True))