import requests


def yahoo_get_api(currency):
    tickers = {
        'USD': 'RUB=X',
        'EUR': 'EURRUB=X',}
    url = f'https://query2.finance.yahoo.com/v10/finance' \
          f'/quoteSummary/{tickers[currency]}?modules=price'
    headers = 'Mozilla/5.0 '
    session = requests.session()
    response = session.get(url, headers={'User-Agent': headers})
    result = dict(response.json())
    currency_rate = result['quoteSummary']['result'][0]['price']['regularMarketPrice']['fmt']
    return currency_rate
