import datetime

from request_currency import yahoo_get_currency
from requests_db import add_history_user, create_user, get_user_info, \
    enrollment_and_write_downs, get_history_user

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
def logic_create_user(user_id: int):
    if create_user(user_id) == 1:
        message = f'Пользователь c id {user_id} успешно создан.'
    elif create_user(user_id) == 0:
        message = f'Пользователь c id {user_id} уже существует.'
    return message


@hadler_logging
def logic_get_user_info(user_id: int, currency: str = 'RUB'):
    currency_list = ['USD', 'EUR']
    try:
        user_info = get_user_info(user_id)[0]
        if user_info:
            message = f'Информация о пользователе с id {user_id}, ' \
                      f'успешно получена.'
            balance = user_info['balance']
        else:
            message = f'Пользователь с id {user_id}, не создан.'
            balance = None
    except Exception as e:
        message = f'Пользователь с id {user_id}, не создан. Исключение: {e}.'
        balance = None
    finally:
        if currency != 'RUB':
            if currency in currency_list and user_info['balance'] is None:
                balance = 0.0
            elif currency in currency_list:
                currency_rate = yahoo_get_currency(currency)
                balance = round(
                    float(user_info['balance']) / currency_rate, 2)
            else:
                message += f' В валюте {currency}, ' \
                           f'невозможно рассчитать баланс'
    return message, balance


@history_transaction_add
@hadler_logging
def logic_transaction(user_id: int, amount: float, purpose: str,
                      enrollment: bool = False, write_down: bool = False):
    user_info = get_user_info(user_id)
    if user_info:
        balance = get_user_info(user_id)[0]['balance']
    else:
        message = f'Невозможно произвести транзакцию, т.к. ' \
                  f'пользователя с id {user_id} нет в базе'
    if balance is None:
        balance = 0.0
    balance = float(balance)
    try:
        if enrollment:
            new_balance = balance + amount
            enrollment_and_write_downs(user_id, new_balance)
            balance = new_balance
            message = f'Успешно пополнен баланс пользователя с id ' \
                      f'{user_id}, на сумму({amount}).'
            if purpose is None:
                purpose = 'Пополнение'
        elif write_down:
            if balance - amount < 0:
                message = f'У пользователся с id {user_id} недостаточно ' \
                          f'средств на балансе, для списания суммы.'
            else:
                new_balance = balance - amount
                enrollment_and_write_downs(user_id, new_balance)
                balance = new_balance
                message = f'У пользователя с id {user_id} успешно списана ' \
                          f'сумма({amount}) с баланса.'
                if purpose is None:
                    purpose = 'Списание'
    except Exception as e:
        message = f'При транзакции произошла ошибка: {e}.'
    finally:
        result = {
            'user_id': user_id,
            'amount': amount,
            'balance': balance,
            'purpose': purpose,
            'message': message
        }
        return result


@hadler_logging
def logic_transaction_user_user(user_donor: int,
                                user_recepient: int,
                                amount: float):
    recepient_info = get_user_info(user_recepient)[0]
    donor_info = get_user_info(user_donor)[0]
    balance = donor_info.get('balance', None)
    if balance is not None:
        balance = float(balance)
    if recepient_info is not None and donor_info is not None:
        if balance is not None \
                and balance >= amount:
            purpose = f'Транзакция от пользователся с id {user_donor} к ' \
                      f'пользователю с id {user_recepient}, на сумму {amount}'
            logic_transaction(
                user_donor, amount, write_down=True, purpose=purpose)
            logic_transaction(
                user_recepient, amount, enrollment=True, purpose=purpose)
            balance = balance - amount
            message = f'{purpose}, проведена успешно.'
        else:
            message = f'У пользователя с id {user_donor} ' \
                      f'не достаточно средств на балансе'
    else:
        user_id = user_donor
        if recepient_info is None:
            user_id = user_recepient
        message = f'Пользователя с id {user_id} не сущесвует.'
    return message, balance


def logic_get_history(user_id: int,
                      sorted_amount: bool = False,
                      sorted_data: bool = False):
    history_list = []
    if get_user_info(user_id)[0]['balance'] is not None:
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
                    'data': transaction['data'].strftime('%Y:%m:%d:%H:%M:%S'),
                    'balance': transaction['balance'],
                    'amount': transaction['amount'],
                    'purpose': transaction['purpose'],
                }
                history_list.append(info_transaction)
    else:
        message = f'История транзакция пользователся с id {user_id}, ' \
                  f'не получена.'
    return message, history_list
