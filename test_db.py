from requests_db import *
import pytest
import pymysql


def test_create_delete_user():
    assert create_user(2999) == 1
    assert get_user_info(2999) == [{'user_id': 2999, 'balance': None}]
    assert delete_user(2999) == 1
    assert delete_user(2999) == 0
    assert get_user_info(2999) == None
    delete_user(2999)


def test_transactions():
    create_user(2999)
    enrollment_and_write_downs(2999, 100.5)
    assert get_user_info(2999) == [{'user_id': 2999, 'balance': 100.5}]
    enrollment_and_write_downs(2999, 0)
    assert get_user_info(2999) == [{'user_id': 2999, 'balance': 0}]
    with pytest.raises(Exception):
        enrollment_and_write_downs(2999, -200)
    delete_user(2999)


def test_history():
    create_user(2999)
    enrollment_and_write_downs(2999, 100.5)
    add_history_user(2999, 100.5, 100.5, 'test1')
    enrollment_and_write_downs(2999, 50.05)
    add_history_user(2999, 50.05, 155.55, 'test2')
    test_case = get_history_user(2999)
    assert float(test_case[0]['balance']) == 100.50
    assert float(test_case[0]['transaction']) == 100.5
    assert test_case[0]['purpose'] == 'test1'
    assert float(test_case[1]['balance']) == 155.55
    assert float(test_case[1]['transaction']) == 50.05
    assert test_case[1]['purpose'] == 'test2'
    delete_user(2999)
    test_case = get_history_user(2999)
    assert test_case == None
