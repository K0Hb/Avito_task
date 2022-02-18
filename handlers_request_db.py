from urllib import response
from requests_db import *


def history_transaction_add(func):
    def wrapper(*args, **qwargs):
        result = func(*args, **qwargs)
        user_id = result['user_id']
        transaction_amount = result['transaction']
        balance = result['balance']
        try:
            add_history_user(user_id, transaction_amount, balance)
            print(f'В историю транзакций пользователся с id {user_id} успешно добавлена информация: изменен баланс на сумму {transaction_amount}.')
        except Exception as e:
            print(f'Произошла ошибка записи в историю транзакция пользователся с id {user_id}.')
            print(e)
        return result
    return wrapper


def handler_create_user(user_id):
    try:
        create_user(user_id)
        return f'Пользователь c id {user_id} успешно создан.'
    except pymysql.err.IntegrityError as e:
        return f'Пользователь c id {user_id} уже существует.'


def handler_user_info(user_id):
    try:
        if all:
            user_info = get_user_info(user_id)
            if user_info:
                message = f'Информация о пользователе с id {user_id}, успешно получена.'
                result =  user_info[0]
            else:
                message = f'Пользователь с id {user_id}, не создан.'
                result =  None
    except Exception as e:
        message = f'Пользователь с id {user_id}, не создан. Исключение: {e}.'
        result = None
    finally:
        response = {
            'user_id' : user_id,
            'user_info' : result,
            'message' : message
        }
        return response 

@history_transaction_add
def handler_transactions(user_id, number, enrollment=False, write_down=False):
    number = float(number)
    balance = handler_user_info(user_id)['user_info']['balance']
    if balance is None:
        balance = 0.0
    balance = float(balance)
    try:
        if enrollment:
            new_balance = balance + number
            enrollment_and_write_downs(user_id, new_balance)
            transaction = number
            balance = new_balance
            message = f'Успешно пополнен баланс пользователя с id {user_id}, на сумму({number}).'
        elif write_down:
            if balance - number <0:
                transaction = 0
                message = f'У пользователся с id {user_id} недостаточно средств на балансе, для списания суммы.'
            else:
                new_balance = balance - number
                enrollment_and_write_downs(user_id, new_balance)
                transaction = -number
                balance = new_balance
                message = f'У пользователя с id {user_id} успешно списана сумма({number}) с баланса.'
    except Exception as e:
        message = f'При транзакции произошла ошибка: {e}.'
    finally:
        response = {
            'user_id' : user_id,
            'balance' : balance,
            'transaction' : transaction,
            'message' : message,
            }
        return response


def handler_transaction_user_user(user_donor, user_recepient, number):
    recepient_info = handler_user_info(user_recepient)['user_info']
    donor_info = handler_user_info(user_donor)['user_info']
    if recepient_info is not None and donor_info is not None:
        if donor_info['balance'] is not None and donor_info['balance'] >= number:
            handler_transactions(user_donor, number, write_down=True)
            handler_transactions(user_recepient, number, enrollment=True)
            message = f'Транзакция от пользователся с id {user_donor} к пользователю с id {user_recepient}, на сумму {number},проведена успешно.'
        else:
            message = f'У пользователя с id {user_donor} не достаточно средств на балансе'
    else:
        user_id = user_donor
        if recepient_info is None:
            user_id = user_recepient
        message = f'Пользователя с id {user_id} не сущесвует.'
    print(message)
    pass


handler_transaction_user_user(2, 1, 100)
# handler_create_user(2)
# print(handler_transactions(2, 200, write_down=True))
# print(handler_user_info(1))
# print(handler_user_info(2))
# handler_create_user(1)