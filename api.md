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

Error Code
==========
- 19001   Rate-limited
- 30004   Invalid parameter
- 30007   Contract not found


Public Endpoints
================
- Public endpoints accept `GET` requests.
- Parameters should be sent as a URL-encoded query string.


Currency List
-------------
```GET https://api.coinx.pro/rest/v1/currencies```

- Response:
```
currencies          array(object)       Currency list
  symbol                string              Currency symbol
  min_deposit_quantity  double              Minimum deposit quantity
  min_withdraw_quantity double              Minimux withdraw quantity (including fee)
  withdraw_flat_fee     double              Withdraw fee
  status                string              Wallet service status, value range:
                                            WORKING
                                            MAINTENANCE
```


Contract List
-------------
``` GET https://api.coinx.pro/rest/v1/contracts```
- Response:
```
contracts           array(object)       Contract list
  symbol            string              Contract symbol
  currency          string              The pricing currency
  commodity         string              The traded currency
  price_tick        double              Minimum price change unit
  lot_size          double              Minimum order quantity unit
  taker_fee_ratio   double              Taker trade fee
  maker_fee_ratio   double              Maker trade fee
```


Price Ticker
------------
```GET /rest/v1/ticker```
- Parameters:
```
symbol              string              Contract symbol
```
- Response:
```
timestamp           int                 Timestamp
last                double              Last price
volume              double              Volume in the last 24 hours
bid                 double              Bid price
ask                 double              Ask price
```


All Price Ticker
----------------
```GET https://api.coinx.pro/rest/v1/all_ticker```

- Response:
Each key of the response JSON object is a contract symbol, and the
corresponding value is in the following format:
```
timestamp           int                 Timestamp
last                double              Last price
volume              double              Volume in the last 24 hours
change              double              Price change percentage in the last 24 hours
bid                 double              Bid price
ask                 double              Ask price
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


Depth
-----
```GET https://api.coinx.pro/rest/v1/depth```

- Parameters:
```
symbol              string              Contract symbol
```

- Response:
```
timestamp           int                 Timestamp
last                double              Last price
bids                array(list)         Bid price levels, each item is a (price, quantity) tuple
asks                array(list)         Ask price levels, each item is a (price, quantity) tuple
```


Recent Trades
-------------
```GET https://api.coinx.pro/rest/v1/trades```

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
  price             double              Price
  volume            double              Volume
```
