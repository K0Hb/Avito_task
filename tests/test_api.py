import json
import pytest
from fastapi.testclient import TestClient

from app.handlers import app
from app.requests_db import delete_user, create_user
from decorator_test import delete_data_test

client = TestClient(app)

TEST_USER = 2999


@delete_data_test(TEST_USER)
def test_craete_user_and_info():
    '''
        Тест проверяет создание пользователся,
        первый раз и на повторное создание.
        (перезаписывть пользователя нельзя).
    '''
    delete_user(TEST_USER)
    response = client.get(f'/create_user/{str(TEST_USER)}')
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Пользователь c id {str(TEST_USER)} успешно создан."
    }
    response = client.get('/create_user/2999')
    case1 = {
        "message": f"Пользователь c id {str(TEST_USER)} уже существует."
    }
    assert response.status_code == 200
    assert response.json() == case1
    response = client.get(f'/user_info/{str(TEST_USER)}')
    case2 = {
        'user_id': TEST_USER,
        'balance': None,
        'cureency': 'RUB',
        'message': 'Информация о пользователе с id 2999, успешно получена.'}
    assert response.status_code == 200
    assert response.json() == case2
    response = client.get(f'/user_info/{str(TEST_USER)}?currency=USD')
    case3 = {
        'user_id': 2999,
        'balance': 0.0,
        'cureency': 'USD',
        'message': 'Информация о пользователе с id 2999, успешно получена.'}
    assert response.status_code == 200
    assert response.json() == case3
    amount = 200.0
    client.get(
        f'/transaction/{str(TEST_USER)}'
        f'?amount={amount}'
        f'&enrollment=true')
    response = client.get(f'/user_info/{str(TEST_USER)}?currency=USD')
    assert response.status_code == 200
    assert response.json()['user_id'] == 2999
    assert response.json()['cureency'] == 'USD'
    assert response.json()['balance'] > 0
    assert response.json()['message'] == case3['message']


@delete_data_test(TEST_USER)
def test_transactions_user():
    '''
    Тест проверят транзакции: зачисление/списание.
    '''
    amount = 200.0
    response = client.get(
        f'/transaction/{str(TEST_USER)}'
        f'?amount={amount}'
        f'&enrollment=true')
    case1 = {
        'user_id': 2999,
        'balance': 200.0,
        'amount': 200.0,
        'message': 'Успешно пополнен баланс пользователя с id 2999,'
                   ' на сумму(200.0).',
        'purpose': 'Пополнение'}
    assert response.status_code == 200
    assert response.json() == case1
    amount = 100.0
    response = client.get(
        f'/transaction/{str(TEST_USER)}'
        f'?amount={amount}'
        f'&write_down=true')
    case2 = {
        'user_id': 2999,
        'balance': 100.0,
        'amount': 100.0,
        'message': 'У пользователя с id 2999 успешно списана'
                   ' сумма(100.0) с баланса.',
        'purpose': 'Списание'}
    assert response.status_code == 200
    assert response.json() == case2
    amount = 101.0
    response = client.get(
        f'/transaction/{str(TEST_USER)}'
        f'?amount={amount}'
        f'&write_down=true')
    case3 = {
        'user_id': 2999,
        'balance': 100.0,
        'amount': 101.0,
        'message': 'У пользователся с id 2999 недостаточно средств'
                   ' на балансе, для списания суммы.',
        'purpose': None}
    assert response.status_code == 200
    assert response.json() == case3


@delete_data_test(TEST_USER)
def test_transaction_user_user():
    '''
    Тест проверяет транзакции между пользователями.
    '''
    amount = 100
    client.get(f'/transaction/{str(TEST_USER)}'
               f'?amount={amount}'
               f'&enrollment=true')
    response = client.get(
        f'/transaction_user_user/{str(TEST_USER)}'
        f'?user_recepient={str(TEST_USER + 1)}'
        f'&amount={amount / 2}')
    case1 = {
        'message': 'Транзакция от пользователся с id 2999 к пользователю с'
                   ' id 3000, на сумму 50.0, проведена успешно.',
        'amount': 50.0,
        'balance': 50.0}
    assert response.status_code == 200
    assert response.json() == case1
    response = client.get(f'/user_info/{str(TEST_USER + 1)}')
    user_info_cas1 = {
        'user_id': 3000,
        'balance': 50.0,
        'cureency': 'RUB',
        'message': 'Информация о пользователе с id 3000, успешно получена.'}
    assert response.status_code == 200
    assert response.json() == user_info_cas1
    response = client.get(
        f'/transaction_user_user/{str(TEST_USER)}'
        f'?user_recepient={str(TEST_USER + 1)}'
        f'&amount={amount}')
    case2 = {
        'message': 'У пользователя с id 2999 не достаточно средств на балансе',
        'amount': 100.0,
        'balance': 50.0}
    assert response.status_code == 200
    assert response.json() == case2


@delete_data_test(TEST_USER)
def test_history_user():
    '''
    Тест на проверу истории транзакций пользователя.
    '''
    amount = 200.0
    client.get(
        f'/transaction/{str(TEST_USER)}?amount={amount}&enrollment=true')
    client.get(
        f'/transaction/{str(TEST_USER)}?amount={amount * 2}&enrollment=true')
    client.get(
        f'/transaction/{str(TEST_USER)}?amount={amount}&write_down=true')
    client.get(
        f'/transaction_user_user/{str(TEST_USER)}'
        f'?user_recepient={str(TEST_USER + 1)}'
        f'&amount={amount / 4}')
    response = client.get(f'/user_history/{str(TEST_USER)}')
    test_case = {
        'message': 'История транзакция пользователся с id 2999, '
                   'успешно получена.',
        'history': [
            {'data': '2022:02:21:11:05:10',
             'balance': 200.0,
             'amount': 200.0,
             'purpose': 'Пополнение'},
            {'data': '2022:02:21:11:05:10',
             'balance': 600.0,
             'amount': 400.0,
             'purpose': 'Пополнение'},
            {'data': '2022:02:21:11:05:10',
             'balance': 400.0,
             'amount': 200.0,
             'purpose': 'Списание'},
            {'data': '2022:02:21:11:05:10',
             'balance': 350.0,
             'amount': 50.0,
             'purpose': 'Транзакция от пользователся с id 2999 к пользователю '
                        'с id 3000, на сумму 50.0'}
        ]
    }
    assert response.status_code == 200
    assert response.json()['message'] == test_case['message']
    for index, transaction in enumerate(response.json()['history']):
        assert test_case['history'][index]['balance'] == transaction['balance']
        assert test_case['history'][index]['amount'] == transaction['amount']
        assert test_case['history'][index]['purpose'] == transaction['purpose']
    response = client.get(f'/user_history/{str(TEST_USER)}?sorted_amount=true')
    assert response.status_code == 200
    response = client.get(f'/user_history/{str(TEST_USER)}?sorted_data=true')
    assert response.status_code == 200
