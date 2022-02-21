import sys
import traceback

from app.requests_db import delete_user, create_user

USER_ID = 2999


def delete_data_test(user_id):
    '''
    Декоратор созданет и удаленет полльзователя,
    для удаления данных из БД,
    независимо от результат тестов.
    '''

    def outer(func):
        def wraper(*args, **qwargs):
            delete_user(user_id)
            delete_user(user_id + 1)
            create_user(user_id)
            create_user(user_id + 1)
            try:
                result = func(*args, **qwargs)
                return result
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)
                tb_info = traceback.extract_tb(tb)
                _, line, _, text = tb_info[-1]

                print(
                    'An error occurred on line '
                    '{} in statement {}'.format(line, text)
                )
                exit(1)
            finally:
                delete_user(user_id)
                delete_user(user_id + 1)

        return wraper

    return outer
