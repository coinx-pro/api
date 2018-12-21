import requests


BASE = 'https://api.coinx.pro'


def get_currency_list():
    endpoint = '/rest/v1/currencies'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_contract_list():
    endpoint = '/rest/v1/contracts'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_price_ticker(symbol):
    endpoint = '/rest/v1/ticker'
    response = requests.get(BASE + endpoint, params={'symbol': symbol})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_all_price_ticker():
    endpoint = '/rest/v1/all_ticker'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_depth(symbol):
    endpoint = '/rest/v1/depth'
    response = requests.get(BASE + endpoint, params={'symbol': symbol})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_recent_trades(symbol, limit=200, after=''):
    endpoint = '/rest/v1/trades'
    response = requests.get(BASE + endpoint, params={'symbol': symbol, 'limit': limit, 'after': after})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


if __name__ == '__main__':
    print("get_currency_list: ",  get_currency_list())

    print("get_contract_list: ", get_contract_list())

    print("get_price_ticker('ETH/BTC'): ", get_price_ticker('ETH/BTC'))

    print("get_all_price_ticker: ",  get_all_price_ticker())

    print("get_recent_trades('ETH/BTC'): ", get_recent_trades('ETH/BTC'))

    print("get_recent_trades('ETH/BTC'): ", get_recent_trades('ETH/BTC'))

