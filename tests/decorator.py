from app.requests_db import delete_user, create_user
import sys
import traceback
USER_ID = 2999


def delete_data_test(func):
    '''
    Декоратор созданет и удаленет полльзователя,
    для удаления данных из БД,
    независимо от результат тестов.
    '''

    def wraper(*args, **qwargs):
        create_user(USER_ID)
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
            delete_user(USER_ID)

    return wraper