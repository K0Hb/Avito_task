from fastapi import FastAPI
import pymysql

from request_currency import yahoo_get_currency
from requests_db import add_history_user, create_user, get_user_info, \
    enrollment_and_write_downs, get_history_user

app = FastAPI()

LOG = False


def hadler_logging(func):
    def wrapper(*args, **qwargs):
        result = func(*args, **qwargs)
        if LOG:
            print(result['message'])
        return result

    return wrapper


def history_transaction_add(func):
    def wrapper(*args, **qwargs):
        result = func(*args, **qwargs)
        user_id = result['user_id']
        transaction_amount = result['amount']
        balance = result['balance']
        purpose = result['purpose']
        try:
            add_history_user(user_id, transaction_amount, balance, purpose)
            message = f'В историю транзакций пользователся с id {user_id} ' \
                      f'успешно добавлена информация: изменен баланс на ' \
                      f'сумму {transaction_amount}.'
        except Exception as e:
            message = f'Произошла ошибка записи в историю транзакция ' \
                      f'пользователся с id {user_id}. Ошибка :{e}'
        finally:
            if LOG:
                print(message)
        return result

    return wrapper


@hadler_logging
@app.get('/create_user/{user_id}')
def handler_create_user(user_id: int):
    if create_user(user_id) == 1:
        message = f'Пользователь c id {user_id} успешно создан.'
    elif create_user(user_id) == 0:
        message = f'Пользователь c id {user_id} уже существует.'
    response = {'message': message}
    return response


@hadler_logging
@app.get('/user_info/{user_id}')
def handler_user_info(user_id: int, currency: str = 'RUB'):
    currency_list = ['USD', 'EUR']
    try:
        user_info = get_user_info(user_id)
        if user_info:
            message = f'Информация о пользователе с id {user_id}, ' \
                        f'успешно получена.'
            result = user_info[0]
        else:
            message = f'Пользователь с id {user_id}, не создан.'
            result = {}
    except Exception as e:
        message = f'Пользователь с id {user_id}, не создан. Исключение: {e}.'
        result = {}
    finally:
        if currency != 'RUB' and currency in currency_list:
            currency_rate = yahoo_get_currency(currency)
            result['balance'] = round(
                float(result['balance']) / currency_rate, 2)
        response = {
            'user_id': user_id,
            'balance': result.get('balance'),
            'cureency': currency,
            'message': message,
        }
        return response


@history_transaction_add
@hadler_logging
@app.get('/transaction/{user_id}')
def handler_transaction(user_id: int,
                        number: float,
                        purpose: str = None,
                        enrollment: bool = False,
                        write_down: bool = False):
    number = float(number)
    balance = handler_user_info(user_id)['balance']
    if balance is None:
        balance = 0.0
    balance = float(balance)
    try:
        if enrollment:
            new_balance = balance + number
            enrollment_and_write_downs(user_id, new_balance)
            transaction = number
            balance = new_balance
            message = f'Успешно пополнен баланс пользователя с id ' \
                      f'{user_id}, на сумму({number}).'
            if purpose is None:
                purpose = 'Пополнение'
        elif write_down:
            if balance - number < 0:
                transaction = 0
                message = f'У пользователся с id {user_id} недостаточно ' \
                          f'средств на балансе, для списания суммы.'
            else:
                new_balance = balance - number
                enrollment_and_write_downs(user_id, new_balance)
                transaction = number
                balance = new_balance
                message = f'У пользователя с id {user_id} успешно списана ' \
                          f'сумма({number}) с баланса.'
                if purpose is None:
                    purpose = 'Списание'
    except Exception as e:
        message = f'При транзакции произошла ошибка: {e}.'
    finally:
        response = {
            'user_id': user_id,
            'balance': balance,
            'amount': transaction,
            'message': message,
            'purpose': purpose
        }
        return response


@hadler_logging
@app.get('/transaction_user_user/{user_id}')
def handler_transaction_user_user(user_donor: int,
                                  user_recepient: int,
                                  number: float):
    recepient_info = handler_user_info(user_recepient)
    donor_info = handler_user_info(user_donor)
    if recepient_info is not None and donor_info is not None:
        if donor_info['balance'] is not None \
                and donor_info['balance'] >= number:
            purpose = f'Транзакция от пользователся с id {user_donor} к ' \
                      f'пользователю с id {user_recepient}, на сумму {number}'
            handler_transaction(
                user_donor, number, write_down=True, purpose=purpose)
            handler_transaction(
                user_recepient, number, enrollment=True, purpose=purpose)
            message = f'{purpose}, проведена успешно.'
        else:
            message = f'У пользователя с id {user_donor} ' \
                      f'не достаточно средств на балансе'
    else:
        user_id = user_donor
        if recepient_info is None:
            user_id = user_recepient
        message = f'Пользователя с id {user_id} не сущесвует.'
    response = {'message': message}
    return response


@hadler_logging
@app.get('/user_history/{user_id}')
def handler_get_history(user_id: int,
                        sorted_amount: bool = False,
                        sorted_data: bool = False):
    history_list = []
    if handler_user_info(user_id)['balance'] is not None:
        try:
            history = get_history_user(user_id,
                                       sorted_amount=sorted_amount,
                                       sorted_data=sorted_data)
            message = f'История транзакция пользователся с' \
                      f' id {user_id}, успешно получена.'
        except Exception as e:
            history = []
            message = f'История транзакция пользователся с' \
                      f' id {user_id}, не получена.Ошибка {e}'
        if history is None:
            message = f'История транзакция пользователся с id {user_id} пустая'
        else:
            for transaction in history:
                info_transaction = {
                    'data': transaction['data'],
                    'balance': transaction['balance'],
                    'amount': transaction['amount'],
                    'purpose': transaction['purpose'],
                }
                history_list.append(info_transaction)
    else:
        message = f'История транзакция пользователся с id {user_id}, ' \
                  f'не получена.'
    response = {'message': message, 'history': history_list}
    return response
