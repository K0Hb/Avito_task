from app.requests_db import *
from test_handlers import delete_data_test
import pytest

USER_ID = 2999


def test_create_delete_user():
    '''
    Тест проверят обработку данных при создание пользователся.
    '''
    assert create_user(USER_ID) == 1
    assert get_user_info(USER_ID) == [{'user_id': 2999, 'balance': None}]
    assert delete_user(USER_ID) == 1
    assert delete_user(USER_ID) == 0
    assert get_user_info(USER_ID) == None
    delete_user(USER_ID)


@delete_data_test
def test_transactions():
    '''
    Тест проверят обработку данных при изменнии баланса пользователся.
    '''
    enrollment_and_write_downs(USER_ID, 100.5)
    assert get_user_info(USER_ID) == [{'user_id': 2999, 'balance': 100.5}]
    enrollment_and_write_downs(USER_ID, 0)
    assert get_user_info(USER_ID) == [{'user_id': 2999, 'balance': 0}]
    with pytest.raises(Exception):
        enrollment_and_write_downs(USER_ID, -200)


@delete_data_test
def test_history():
    '''
    Тест проверят обработку данных истории транзакций.
    '''
    enrollment_and_write_downs(USER_ID, 100.5)
    add_history_user(USER_ID, 100.5, 100.5, 'test1')
    enrollment_and_write_downs(USER_ID, 50.05)
    add_history_user(USER_ID, 50.05, 155.55, 'test2')
    test_case = get_history_user(USER_ID)
    assert float(test_case[0]['balance']) == 100.50
    assert float(test_case[0]['transaction']) == 100.5
    assert test_case[0]['purpose'] == 'test1'
    assert float(test_case[1]['balance']) == 155.55
    assert float(test_case[1]['transaction']) == 50.05
    assert test_case[1]['purpose'] == 'test2'
    delete_user(USER_ID)
    test_case = get_history_user(USER_ID)
    assert test_case == None
