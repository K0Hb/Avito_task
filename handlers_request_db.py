from requests_db import *


def history_transaction_add(func):
    def wrapper(*args, **qwargs):
        result = func(*args, **qwargs)
        user_id = result['user_id']
        transaction_amount = result['transaction']
        balance = result['balance']
        try:
            add_history_user(user_id, transaction_amount, balance)
            print(f'В историю транзакций пользователся с id {user_id} успешно добавлена информация: изменен баланс на сумму {transaction_amount}')
        except Exception as e:
            print(f'Произошла ошибка записи в историю транзакция пользователся с id {user_id}')
            print(e)
        return result
    return wrapper


def handler_create_user(user_id):
    try:
        create_user(user_id)
        return f'Пользователь c id {user_id} успешно создан'
    except pymysql.err.IntegrityError as e:
        return f'Пользователь c id {user_id} уже существует'


def handler_user_info(user_id):
    try:
        if all:
            user_info = get_user_info(user_id)
            if user_info:
                return user_info[0]
            else:
                return f'Пользователь с id {user_id}, не создан'
    except Exception as e:
            return f'При запросе произошла ошибка: {e}'

@history_transaction_add
def handler_transactions(user_id, number, enrollment=False, write_down=False):
    number = float(number)
    balance = float(handler_user_info(user_id)['balance'])
    if balance is None:
        balance = 0.0
    try:
        if enrollment:
            new_balance = balance + number
            enrollment_and_write_downs(user_id, new_balance)
            transaction = number
            balance = new_balance
            message = f'Успешно пополнен баланс пользователя с id {user_id}, на сумму({number})'
        elif write_down:
            if balance - number <0:
                transaction = 0
                message = f'У пользователся с id {user_id} недостаточно средств на балансе, для списания суммы'
            else:
                new_balance = balance - number
                enrollment_and_write_downs(user_id, new_balance)
                transaction = -number
                balance = new_balance
                message = f'У пользователя с id {user_id} успешно списана сумма({number}) с баланса'
    except Exception as e:
        message = f'При транзакции произошла ошибка: {e}'
    finally:
        response = {
            'user_id' : user_id,
            'balance' : balance,
            'transaction' : transaction,
            'message' : message,
            }
        return response

# handler_create_user(2)
print(handler_transactions(2, 200, write_down=True))
print(handler_user_info(2))