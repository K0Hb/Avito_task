<a href="https://codeclimate.com/github/K0Hb/Avito_task/maintainability"><img src="https://api.codeclimate.com/v1/badges/97376614187286510812/maintainability" /></a>


### Установка:
- `pip install https://github.com/K0Hb/Avito_task.git` - скачиваем проект
- в файл `env` прописать свои парамерты по примеру `env(example)` для БД (Mysql)
- `pip install poetry` установка зависимостей
- `make run` запуск микросервиса

# Avito_task

Реализован микросервис для работы с балансом пользователей (зачисление средств, списание средств, перевод средств от пользователя к пользователю, а также метод получения баланса пользователя). Сервис предоставляет HTTP API и принимает/отдавает запросы/ответы в формате JSON.

## Список запросов API:
- `http://domain/create_user/{user_id:int}`
    Создаем пользователя
- `http://domain/user_info/{user_id:int}`
    Получаем информацию о пользвателе (id, баланс). Валюта по умолчанию рубль.
- `http://domain/user_info/{user_id:int}?currency={currency:str}`
    Получаем инфомацию о пользователе (id, баланс),  в валюте. Пока реализованы основные: RUB, USD, EUR.
- `http://domain/transaction/{user_id:int}?number={amount : float}&purpose={purpose : str}&enrollment={enrollment : bool}`
    Произвести транзаккцию(пополнение). Назначение не обязательно, есть статусы по умолчанию.
- `http://domain/transaction/{user_id:int}?number={amount : float}&purpose={purpose : str}&write_down={write_down : bool}`
    Произвести транзаккцию(списание). Назначение не обязательно, есть статусы по умолчанию.
- `http://domain/transaction_user_user/{user_id : int}?user_donor={user_donor : int}&user_recepient={user_recepient : int}&number={amount : float}`
    Прозивести транзакцию между пользователями.
- `http://domain/user_history/{user_id : int}`
    Получить историю транзакций.
- `http://domain/user_history/{user_id : int}?sorted_amount={sorted_amount : bool}`
    Получить историю транзакций, отстортированную по сумме транзакции.
- `http://domain/user_history/{user_id : int}?sorted_data={sorted_data : bool}`
    Получить историю транзакций, отстортированную по дате транзакции.

## Дополнительное описание:

- Для тестирования кода, были реализованы методы создания и удаления пользователя.
- Источник для получения информации валюты: Yahoo API.

