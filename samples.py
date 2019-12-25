import hashlib
import hmac
import json
import time
import requests


BASE = 'https://api.coinx.pro'
API_KEY = '0juilzZNuSULN6cyFqj4BBTxqNfLUlVTvWjQnmBV5fyb6ujQA7r6P0vGS3oXUfYk'
API_SECRET = 'oEpxfe0KzA73D7Tgz2pokT3bOhRWKakoS4XXBhPlBxS3s2ffFb6QOzReckM3W2Id'


def get_currency_list():
    endpoint = '/rest/v2/currencies'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_contract_list():
    endpoint = '/rest/v2/contracts'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_price_ticker(symbol):
    endpoint = '/rest/v2/ticker'
    response = requests.get(BASE + endpoint, params={'symbol': symbol})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_all_price_ticker():
    endpoint = '/rest/v2/all_ticker'
    response = requests.get(BASE + endpoint)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_depth(symbol):
    endpoint = '/rest/v2/depth'
    response = requests.get(BASE + endpoint, params={'symbol': symbol})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def get_recent_trades(symbol, limit=200, after=''):
    endpoint = '/rest/v2/trades'
    response = requests.get(BASE + endpoint, params={'symbol': symbol, 'limit': limit, 'after': after})
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


# Authenticated Endpoints
# =======================


def wrap_post_headers_and_body(data):
    data['timestamp'] = int(time.time() * (10 ** 6))
    body = json.dumps(data)
    headers = {
        'X-API-KEY': API_KEY,
        'X-API-SIGNATURE': hmac.new(key=API_SECRET.encode(), msg=body.encode(), digestmod=hashlib.sha256).hexdigest()
    }
    return headers, body


def gen_order(contract, price, quantity, side):
    data = {
        'contract': contract,
        'price': str(price),
        'quantity': str(quantity),
        'side': side,
    }
    return data


def place_order(contract, price, quantity, side):
    endpoint = '/rest/v2/place'
    data = gen_order(contract, price, quantity, side)
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def place_multiple_order(order_list):
    endpoint = '/rest/v2/multi_place'
    data = {
        'place': order_list,
    }
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def cancel_order(contract, uuid):
    endpoint = '/rest/v2/cancel'
    data = {
        'contract': contract,
        'uuid': uuid,
    }
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def cancel_multiple_order(order_list):
    endpoint = '/rest/v2/multi_cancel'
    data = {
        'cancel': order_list,
    }
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def view_order_status(uuid):
    endpoint = '/rest/v2/order_status'
    data = {
        'uuid': uuid
    }
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def view_active_orders():
    endpoint = '/rest/v2/active_orders'
    data = {}
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def view_balance():
    endpoint = '/rest/v2/balance'
    data = {}
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
    if response.ok:
        return response.json()
    else:
        raise Exception(response.content)


def view_history_orders(contract, limit=200):
    endpoint = '/rest/v2/history_orders'
    data = {
        'contract': contract,
        'limit': limit,
    }
    headers, body = wrap_post_headers_and_body(data)
    response = requests.post(BASE + endpoint, headers=headers, data=body)
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

    result = place_order(contract='ETH/BTC', price=0.00001, quantity=0.01, side='BUY')
    print("place_order: ", result)
    print("cancel_order: ", cancel_order(contract=result['contract'], uuid=result['uuid']))
    print("view_order_status: ", view_order_status(result['uuid']))

    place = [
        gen_order(contract='ETH/BTC', price=0.55, quantity=0.01, side='SELL'),
        gen_order(contract='BTC/USDT', price=1000.0, quantity=0.001, side='BUY'),
    ]
    result = place_multiple_order(place)
    print("place_multiple_order: ", result)
    print("cancel_multiple_order: ", cancel_multiple_order([{'contract': x['contract'], 'uuid': x['uuid']} for x in result['result']]))

    print("view_active_orders: ", view_active_orders())

    print("view_balance: ", view_balance())

    print("view_history_orders: ", view_history_orders('ETH/BTC'))
