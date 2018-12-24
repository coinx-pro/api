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
```GET https://api.coinx.pro/rest/v1/ticker```

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

- Request example:
``` GET https://api.coinx.pro/rest/v1/ticker?symbol=BTC/USDT```

- Response example:
```
{
    "ask": 4020.79,
    "timestamp": 1545377083173003,
    "volume": 96.74439,
    "last": 3970.58,
    "bid": 3919.97
}
```


All Price Ticker
----------------
```GET https://api.coinx.pro/rest/v1/tickers```

- Response:
```
data                  array(object)       Price Tickers list
  contract            string              Contract symbol
  commodity           string              Commodity symbol
  currency            string              Currency symbol
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
        }
    ]
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
