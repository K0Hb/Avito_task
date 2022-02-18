import requests


def yahoo_get_currency(currency):
    tickers = {
        'USD': 'RUB=X',
        'EUR': 'EURRUB=X',}
    url = f'https://query2.finance.yahoo.com/v10/finance' \
          f'/quoteSummary/{tickers[currency]}?modules=price'
    headers = 'Mozilla/5.0 '
    try:
        session = requests.session()
        response = session.get(url, headers={'User-Agent': headers})
    except Exception as e:
        print(f'Соеденение с Yahoo API, не удалось')
        result = 0
        return result
    result = dict(response.json())
    currency_rate = float(result['quoteSummary']['result'][0]['price']['regularMarketPrice']['fmt'])
    return currency_rate
