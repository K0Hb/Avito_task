from handlers import *
from requests_db import delete_user


def test_create_user():
    user_id = 2999
    assert handler_create_user(user_id) == {'message': 'Пользователь c id 2999 успешно создан.'}
    assert handler_create_user(user_id) == {'message': 'Пользователь c id 2999 уже существует.'}
    delete_user(2999)


def test_transactions_user():
    user_id = 2999
    handler_create_user(user_id)
    response_case1 = {
        'user_id': 2999,
        'balance': 100.5,
        'transaction': 100.5,
        'message': 'Успешно пополнен баланс пользователя с id 2999, на сумму(100.5).',
        'purpose': 'test1'
        }
    info_case1 = {
        'user_id': 2999,
        'balance': 100.50
    }
    assert handler_transaction(user_id, 100.5, 'test1', enrollment=True) == response_case1
    assert get_user_info(user_id)[0]['user_id'] == info_case1['user_id']
    assert float(get_user_info(user_id)[0]['balance']) == info_case1['balance']
    response_case2 = {
        'user_id': 2999,
        'balance': 50.0,
        'transaction': 50.5,
        'message': 'У пользователя с id 2999 успешно списана сумма(50.5) с баланса.',
        'purpose': 'test2'
        }
    info_case2 = {
        'user_id': 2999,
        'balance': 50.0
    }
    assert handler_transaction(user_id, 50.5, 'test2', write_down=True) == response_case2
    assert get_user_info(user_id)[0]['user_id'] == info_case2['user_id']
    assert float(get_user_info(user_id)[0]['balance']) == info_case2['balance']
    delete_user(2999)


def test_history_user():
    user_id = 2999
    handler_create_user(user_id)
    handler_transaction(user_id, 100.5, 'test1', enrollment=True)
    handler_transaction(user_id, 50.5, 'test2', write_down=True)
    history = handler_get_history(user_id)
    transaction1 = {
        'balance': 100.50,
        'amount': '100.5',
        'purpose': 'test1'
        }
    transaction2 = {
        'balance': 50.00,
        'amount': '50.5',
        'purpose': 'test2'}
    assert float(history['history'][0]['balance']) == transaction1['balance']
    assert history['history'][0]['amount'] == transaction1['amount']
    assert history['history'][0]['purpose'] == transaction1['purpose']
    assert float(history['history'][1]['balance']) == transaction2['balance']
    assert history['history'][1]['amount'] == transaction2['amount']
    assert history['history'][1]['purpose'] == transaction2['purpose']
    delete_user(2999)