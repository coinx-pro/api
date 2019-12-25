General
=======

- All endpoints return a JSON object.

- All timestamp are in microseconds (0.000001 second).

- Any endpoint may return an error in the following format:

```
{
    "error": 30001,
    "error_msg": "optional human-readable error message"
}
```

- Error codes are listed below.

- For `POST` endpoints, parameters should be sent as a JSON object
  in the request body.


Authentication
==============

Each `POST` endpoint must be properly signed by an API key and secret.

- Include a ```timestamp``` parameter in the request, which is the current
  UNIX timestamp in microseconds. The server will only accept a request
  if its timestamp is in a small time window according to server time.
  Currently, the time window size is +/- 1 minute, which is subject to change.

- Send API key as HTTP header ```X-API-KEY```.

- Sign the request body by HMAC-SHA256 with the API secret as key,
  and send the signature hex digest as HTTP header ```X-API-SIGNATURE```.

Here is an example to query an order status:

- The API key:

```
API Key: 0123456789012345678901234567890123456789012345678901234567890123
API Secret: abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcd
```

- The request body:

```
{"uuid":"12345678-abcd-1234-1234-12345678abcd","timestamp":151476480000000000}
```

- Sign the request with openssl:

```
[linux]$ echo -n '{"uuid":"12345678-abcd-1234-1234-12345678abcd","timestamp":151476480000000000}' | openssl dgst -sha256 -hmac "abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcd"
(stdin)= 77ceb2ceb9d4dde8ea01b35df7c97efb602354dc590c2291fe8e2d853b64be43
```

- Send the request with curl:

```
[linux]$ curl -H "X-API-KEY: 0123456789012345678901234567890123456789012345678901234567890123" -H "X-API-SIGNATURE: 77ceb2ceb9d4dde8ea01b35df7c97efb602354dc590c2291fe8e2d853b64be43" -X POST 'https://api.example.com/rest/v2/order_status' -d '{"uuid":"12345678-abcd-1234-1234-12345678abcd","timestamp":151476480000000000}'
```


Error Code
==========

```
19001   Rate-limited

20000   Unknown error
20001   Market closed
20002   Illegal currency
20003   Withdrawal failed due to error of handling fee
20004   Withdrawal failed due to not meet requirement of minimum withdrawal
20005   Insufficient balance
20006   Operator not allowed in the current trade session
21002   Order failed. There is no limit price.
21003   Order failed. There is no stop price.
21004   Order failed. Incorrect entrust validity signal.
21005   Order failed. No stop condition fill in.
21006   Order failed. Incorrect trade direction.
21007   Order failed. Quantity is less than minimum requirement.
21008   Order failed. Incorrect order type.
21009   Order failed. Price should be an integral multiple of price unit.
21010   Order failed. Orders should be an integral multiple of order unit.
21011   Order failed. Insufficient currency.
21012   Order failed. Insufficient commodity.
22000   Cancelation failed. The order does not exist.

30001   Missing X-API-KEY or X-API-SIGNATURE header
30002   Invalid API key or signature
30003   Request body is not a well-formed JSON
30004   Invalid parameter
30005   Order not found
30006   Request is expired (timestamp is too old or too new)
30007   Contract not found
30008   Maximum item count exceeded in batch request
```


Public Endpoints
================

- Public endpoints accept `GET` requests.

- Parameters should be sent as a URL-encoded query string.

Currency List
-------------

```
GET /rest/v2/currencies
```

- Parameters: None

- Response:

```
currencies          array(object)       Currency list
  symbol            string              Currency symbol
  min_deposit_quantity
                    string              Minimum deposit quantity
  min_withdraw_quantity
                    string              Minimux withdraw quantity (including fee)
  withdraw_flat_fee string              Withdraw fee
  status            string              Wallet service status, value range:
                                            WORKING
                                            MAINTENANCE
```

Contract List
-------------

```
GET /rest/v2/contracts
```

- Parameters: None

- Response:

```
contracts           array(object)       Contract list
  symbol            string              Contract symbol
  currency          string              The pricing currency
  commodity         string              The traded currency
  price_tick        string              Minimum price change unit
  lot_size          string              Minimum order quantity unit
  taker_fee_ratio   string              Taker trade fee
  maker_fee_ratio   string              Maker trade fee
```

History K Line
-------------

```
GET /rest/v2/kline
```

- Parameters:

```
symbol              string              Contract symbol
span                int                 Optional, default: 1. The period of each candle, value range:
                                            1,
                                            5,
                                            15,
                                            30,
                                            60,
                                            1440
limit               int                 Optional, default: 20, max: 100. The max number of data returns
cursor              int                 Optional, default: ''
                                        Only returns K Lines before timestamp ```cursor```
```

- Response:

```
cursor              int                 The timestamp of last kline in data
data                array(object)       Contract list
  open              string              Opening price
  close             string              Closing price
  high              string              High price
  low               string              Low price
  volume            string              Volume
  timestamp         int                 Timestamp
```

Price Ticker
------------

```
GET /rest/v2/ticker
```

- Parameters:

```
symbol              string              Contract symbol
```

- Response:

```
timestamp           int                 Timestamp
last                string              Last price
volume              string              Volume in the last 24 hours
bid                 string              Bid price
ask                 string              Ask price
```

All Price Ticker
----------------

```
GET /rest/v2/all_ticker
```

- Parameters: None

- Response:

Each key of the response JSON object is a contract symbol, and the
corresponding value is in the following format:

```
timestamp           int                 Timestamp
last                string              Last price
volume              string              Volume in the last 24 hours
change              string              Price change percentage in the last 24 hours
bid                 string              Bid price
ask                 string              Ask price
```

- Response example:

```
{
    "BTC/USDT": {
        "timestamp": 1514736000000000,
        "ask": 6666.66,
        "bid": 6655.55,
        "change": 23.08,
        "last": 6666.66,
        "volume": 523.10
    },
    "ETH/USDT": {
        "timestamp": 1514736000000000,
        "ask": 488.88,
        "bid": 487.12,
        "change": 4.25,
        "last": 487.12,
        "volume": 8242.35
    }
}
```

Price Tickers
----------------

```
GET /rest/v2/tickers
```

- Parameters: None

- Response:

```
data                  array(object)       Price Tickers list
  contract            string              Contract symbol
  commodity           string              Commodity symbol
  currency            string              Currency symbol
  timestamp           int                 Timestamp
  last                string              Last price
  volume              string              Volume in the last 24 hours
  change              string              Price change percentage in the last 24 hours
  bid                 string              Bid price
  ask                 string              Ask price
```

- Response example:

```
{
    "data": [
        {
            "contract": "ETH/BTC",
            "commodity": "ETH",
            "currency": "BTC",
            "last": 0.02734, "volume": 0.0,
            "change": 0.0, "timestamp": 1545616877117472,
            "bid": 0.02633, "ask": 0.02835
        },
        {
            "contract": "BTC/USDT",
            "commodity": "BTC",
            "currency": "USDT",
            "last": 4135.28,
            "volume": 111.57573,
            "change": 4.2993124530243385,
            "timestamp": 1545616877216149,
            "bid": 4081.48,
            "ask": 4193.47
        }]
}
```

Depth
-----

```
GET /rest/v2/depth
```

- Parameters:

```
symbol              string              Contract symbol
```

- Response:

```
timestamp           int                 Timestamp
last                string              Last price
bids                array(list)         Bid price levels, each item is a (price, quantity) tuple
asks                array(list)         Ask price levels, each item is a (price, quantity) tuple
```

Recent Trades
-------------

```
GET /rest/v2/trades
```

- Parameters:

```
symbol              string              Contract symbol
limit               int                 Optional, default: 200, max: 200
                                        Return at most ```limit``` trades
after               string              Optional, default: ''
                                        Only returns trades after the one with uuid ```after```
```

- Response:

```
trades              array(object)       Trade list
  uuid              string              Trade UUID
  timestamp         int                 Trade timestamp
  side              string              Taker order side, value range: BUY, SELL
  price             string              Price
  volume            string              Volume
```

Authenticated Endpoints
=======================

Place Order
-----------

```
POST /rest/v2/place
```

- Parameters:

```
contract            string              Contract symbol
price               string              Price
quantity            string              Quantity
side                string              Side, value range: BUY, SELL
```

- Response:

```
uuid                string              Order UUID
contract            string              Contract symbol
price               string              Price
quantity            string              Quantity
side                string              Side, value range: BUY, SELL
```

Place Multiple Order
--------------------

```
POST /rest/v2/multi_place
```

Place multiple orders in a batch. No more than 5 orders can be placed in a
single request. If the request is well-formed (e.g. properly signed and having
valid timestamp), results of the orders are returned in a list.

- Parameters:

```
place               array(object)       Order list.
                                        Each element should contain parameters
                                        required by the "Place Order" endpoint.
```

- Response:

```
result              array(object)       Result list.
                                        Each element contains information
                                        given by "Place Order".
```

Cancel Order
------------

```
POST /rest/v2/cancel
```

- Parameters:

```
contract            string              Contract symbol
uuid                string              Order UUID
```

- Response: None

Cancel Multiple Order
---------------------

```
POST /rest/v2/multi_cancel
```

Cancel multiple orders in a batch. No more than 5 orders can be canceled in a
single request. If the request is well-formed (e.g. properly signed and having
valid timestamp), results of the cancels are returned in a list.

- Parameters:

```
cancel              array(object)       Cancel list.
                                        Each element should contain parameters
                                        required by the "Cancel Order" endpoint.
```

- Response:

```
result              array(object)       Result list.
                                        Each element contains information
                                        given by "Cancel Order".
```

Order Status
------------

```
POST /rest/v2/order_status
```

- Parameters:

```
uuid                string              Order UUID
```

- Response:

```
uuid                string              Order UUID
contract            string              Contract symbol
status              string              Order status, value range:
                                            QUEUEING
                                            PARTIAL_FILLED
                                            FILLED
                                            CANCELED
side                string              Side, value range: BUY, SELL
price               string              Price
quantity            string              Quantity
unfilled            string              Unfilled quantity
timestamp           int                 Timestamp when the order is placed
```

Active orders
-------------

```
POST /rest/v2/active_orders
```

- Parameters: None

- Response:

```
orders              array(object)       Order list
  uuid              string              Order UUID
  contract          string              Contract symbol
  status            string              Order status, value range:
                                            QUEUEING
                                            PARTIAL_FILLED
  side              string              Side, value range: BUY, SELL
  price             string              Price
  quantity          string              Quantity
  unfilled          string              Unfilled quantity
  timestamp         int                 Timestamp when the order is placed
```

Balance
-------

```
POST /rest/v2/balance
```

- Parameters: None

- Response:

```
balance             array(object)       Balance list
  currency          string              Currency symbol
  available         string              Available quantity
  frozen            string              Frozen quantity (frozen by order and withdraw)
```

History Orders
--------------

```
POST /rest/v2/history_orders
```

Return recent orders in the given contract, include both active and inactive ones.

WARNING: This endpoint is very costy on the server side, and will have a
strict rate-limit in the future. Orders placed or changed in the last few
seconds may not reflected in the response.

- Parameters:

```
contract            string              Contract symbol
limit               int                 Optional, default: 200, max: 200
                                        Return at most ```limit``` orders
```

- Response:

```
result              array(object)       Result list.
                                        Each element contains information
                                        given by "Cancel Order".
```
