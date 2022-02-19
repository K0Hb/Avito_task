from app.handlers import *
from requests_db import delete_user, create_user
import sys
import traceback


USER_ID = 2999

def delete_data_test(func):
    '''
    Декоратор созданет и удаленет полльзователя,
    для удаления данных из БД,
    независимо от результат тестов
    '''
    def wraper(*args, **qwargs):
        create_user(USER_ID)
        try:
            result = func(*args, **qwargs)
            return result
        except AssertionError as e:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb) # Fixed format
            tb_info = traceback.extract_tb(tb)
            _, line, _, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(line, text))
            exit(1)
        finally:
            delete_user(USER_ID)
    return wraper


def test_create_user():
    '''
    Тест проверяет создание пользователся в БД,
    первый раз и на повторное создание.
    (перезаписывть пользователя нельзя)
    '''
    assert handler_create_user(USER_ID) == {'message': 'Пользователь c id 2999 успешно создан.'}
    assert handler_create_user(USER_ID) == {'message': 'Пользователь c id 2999 уже существует.'}
    delete_user(USER_ID)


@delete_data_test
def test_transactions_user():
    '''
    Тест проверят транзакции: зачисление/списание в БД.
    '''
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
    assert handler_transaction(USER_ID, 100.5, 'test1', enrollment=True) == response_case1
    assert get_user_info(USER_ID)[0]['user_id'] == info_case1['user_id']
    assert float(get_user_info(USER_ID)[0]['balance']) == info_case1['balance']
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
    assert handler_transaction(USER_ID, 50.5, 'test2', write_down=True) == response_case2
    assert get_user_info(USER_ID)[0]['user_id'] == info_case2['user_id']
    assert float(get_user_info(USER_ID)[0]['balance']) == info_case2['balance']



@delete_data_test
def test_history_user():
    '''
    Тест на проверу истории транзакций пользователя в БД
    '''
    handler_create_user(USER_ID)
    handler_transaction(USER_ID, 100.5, 'test1', enrollment=True)
    handler_transaction(USER_ID, 50.5, 'test2', write_down=True)
    history = handler_get_history(USER_ID)
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


import sys
import traceback

def test_transaction_user_user():
    create_user(2999)
    create_user(3000)
    test_message1 = 'Транзакция от пользователся с id 2999 к пользователю с id 3000, на сумму 1000, проведена успешно.'
    test_message2 = 'У пользователя с id 2999 не достаточно средств на балансе'
    try:
        handler_transaction(2999, 1001, 'test1', enrollment=True)
        assert handler_transaction_user_user(2999, 3000, 1000)['message'] == test_message1
        assert float(get_user_info(2999)[0]['balance']) == 1.0
        assert float(get_user_info(3000)[0]['balance']) == 1000.0
        assert handler_transaction_user_user(2999, 3000, 2.0)['message'] == test_message2
    except AssertionError as e:
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb) # Fixed format
        tb_info = traceback.extract_tb(tb)
        _, line, _, text = tb_info[-1]

        print('An error occurred on line {} in statement {}'.format(line, text))
        exit(1)
    finally:
        delete_user(2999)
        delete_user(3000)