from requests_db import *
from request_currency import yahoo_get_currency
from fastapi import FastAPI


app = FastAPI()


LOG = True

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
        transaction_amount = result['transaction']
        balance = result['balance']
        purpose = result['purpose']
        try:
            add_history_user(user_id, transaction_amount, balance, purpose)
            message = f'В историю транзакций пользователся с id {user_id} успешно добавлена информация: изменен баланс на сумму {transaction_amount}.'
        except Exception as e:
            message = f'Произошла ошибка записи в историю транзакция пользователся с id {user_id}. Ошибка :{e}'
        finally:
            if LOG:
                print(message)
        return result
    return wrapper


@hadler_logging
def handler_create_user(user_id):
    try:
        create_user(user_id)
        message = f'Пользователь c id {user_id} успешно создан.'
    except pymysql.err.IntegrityError:
        message =  f'Пользователь c id {user_id} уже существует.'
    finally:
        response = {'message' : message}
        return response

@app.get('/')
@hadler_logging
def handler_user_info(user_id, currency='RUB'):
    currency_list = ['USD', 'EUR']
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
        if currency != 'RUB' and currency in currency_list:
            currency_rate = yahoo_get_currency(currency)
            result['balance'] =  round(float(result['balance']) / currency_rate, 2)
        response = {
            'user_id' : user_id,
            'balance' : result['balance'],
            'cureency' : currency,
            'message' : message,
        }
        return response 


@history_transaction_add
@hadler_logging
def handler_transactions(user_id, number, purpose=None, enrollment=False, write_down=False):
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
            message = f'Успешно пополнен баланс пользователя с id {user_id}, на сумму({number}).'
            if purpose is None:
                purpose = 'Пополнение'
        elif write_down:
            if balance - number <0:
                transaction = 0
                message = f'У пользователся с id {user_id} недостаточно средств на балансе, для списания суммы.'
            else:
                new_balance = balance - number
                enrollment_and_write_downs(user_id, new_balance)
                transaction = number
                balance = new_balance
                message = f'У пользователя с id {user_id} успешно списана сумма({number}) с баланса.'
                if purpose is None:
                    purpose = 'Списание'
    except Exception as e:
        message = f'При транзакции произошла ошибка: {e}.'
    finally:
        response = {
            'user_id' : user_id,
            'balance' : balance,
            'transaction' : transaction,
            'message' : message,
            'purpose' : purpose
            }
        return response


@hadler_logging
def handler_transaction_user_user(user_donor, user_recepient, number):
    recepient_info = handler_user_info(user_recepient)['balance']
    donor_info = handler_user_info(user_donor)['balance']
    if recepient_info is not None and donor_info is not None:
        if donor_info['balance'] is not None and donor_info['balance'] >= number:
            purpose = f'Транзакция от пользователся с id {user_donor} к пользователю с id {user_recepient}, на сумму {number}'
            handler_transactions(user_donor, number, write_down=True, purpose=purpose)
            handler_transactions(user_recepient, number, enrollment=True, purpose=purpose)
            message = f'{purpose}, проведена успешно.'
        else:
            message = f'У пользователя с id {user_donor} не достаточно средств на балансе'
    else:
        user_id = user_donor
        if recepient_info is None:
            user_id = user_recepient
        message = f'Пользователя с id {user_id} не сущесвует.'
    response = {'message' : message}
    return response


@hadler_logging
def handler_get_history(user_id, sorted_amount=False, sorted_data=False):
    history_dict = {}
    if handler_user_info(user_id)['balance'] is not None:
        try:
            history = get_history_user(user_id, sorted_amount=sorted_amount, sorted_data=sorted_data)
            message = f'История транзакция пользователся с id {user_id}, успешно получена.'
        except Exception as e:
            history = []
            message = f'История транзакция пользователся с id {user_id}, не получена.Ошибка {e}'

        for index, transaction in enumerate(history):
            info_transaction = {
                'data' : transaction['data'],
                'balance' : transaction['balance'],
                'amount' : transaction['transaction'],
                'purpose' : transaction['purpose'],
            }
            history_dict[index] = info_transaction
    else:
        message = f'История транзакция пользователся с id {user_id}, не получена.'
    response = {'message' : message, 'history' : history_dict}
    return response


# handler_get_history(2)
# handler_create_user(3)
# handler_transactions(2, 5000.50, enrollment=True)
# print(handler_user_info(1))
print(handler_user_info(2, currency='USD'))
# handler_create_user(1)
# handler_transaction_user_user(2,3, 200.03)