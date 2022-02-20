from fastapi import FastAPI

from main_logic import logic_create_user, logic_get_user_info,\
    logic_transaction, logic_transaction_user_user, logic_get_history

LOG = False
app = FastAPI()


@app.get('/create_user/{user_id}')
def handler_create_user(user_id: int):
    response = {'message': logic_create_user(user_id)}
    return response


@app.get('/user_info/{user_id}')
def handler_user_info(user_id: int, currency: str = 'RUB'):
    message, balance = logic_get_user_info(user_id, currency)
    response = {
        'user_id': user_id,
        'balance': balance,
        'cureency': currency,
        'message': message,
    }
    return response


@app.get('/transaction/{user_id}')
def handler_transaction(user_id: int,
                        amount: float,
                        purpose: str = None,
                        enrollment: bool = False,
                        write_down: bool = False):
    transaction_info = logic_transaction(
        user_id, amount, purpose, enrollment, write_down)
    response = {
        'user_id': user_id,
        'balance': transaction_info['balance'],
        'amount': amount,
        'message': transaction_info['message'],
        'purpose': transaction_info['purpose']
    }
    return response


@app.get('/transaction_user_user/{user_id}')
def handler_transaction_user_user(user_donor: int,
                                  user_recepient: int,
                                  amount: float):
    message, balance = logic_transaction_user_user(
        user_donor, user_recepient, amount)
    response = {'message': message,
                'amount': amount,
                'balance': balance
                }
    return response


@app.get('/user_history/{user_id}')
def handler_get_history(user_id: int,
                        sorted_amount: bool = False,
                        sorted_data: bool = False):
    message, history_list = logic_get_history(
        user_id, sorted_amount, sorted_data)
    response = {'message': message, 'history': history_list}
    return response
