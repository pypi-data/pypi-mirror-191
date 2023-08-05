# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class btcturk(Exchange):

    def describe(self):
        return self.deep_extend(super(btcturk, self).describe(), {
            'id': 'btcturk',
            'name': 'BTCTurk',
            'countries': ['TR'],  # Turkey
            'rateLimit': 100,
            'has': {
                'CORS': True,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
            },
            'timeframes': {
                '1m': 1,
                '15m': 15,
                '30m': 30,
                '1h': 60,
                '4h': 240,
                '1d': '1 day',
                '1w': '1 week',
                '1y': '1 year',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87153926-efbef500-c2c0-11ea-9842-05b63612c4b9.jpg',
                'api': {
                    'public': 'https://api.btcturk.com/api/v2',
                    'private': 'https://api.btcturk.com/api/v1',
                    'graph': 'https://graph-api.btcturk.com/v1',
                },
                'www': 'https://www.btcturk.com',
                'doc': 'https://github.com/BTCTrader/broker-api-docs',
            },
            'api': {
                'public': {
                    'get': {
                        'orderbook': 1,
                        'ticker': 0.1,
                        'trades': 1,   # ?last=COUNT(max 50)
                        'server/exchangeinfo': 1,
                    },
                },
                'private': {
                    'get': {
                        'users/balances': 1,
                        'openOrders': 1,
                        'allOrders': 1,
                        'users/transactions/trade': 1,
                    },
                    'post': {
                        'order': 1,
                        'cancelOrder': 1,
                    },
                    'delete': {
                        'order': 1,
                    },
                },
                'graph': {
                    'get': {
                        'ohlcs': 1,
                        'klines/history': 1,
                    },
                },
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.0005'),
                    'taker': self.parse_number('0.0009'),
                },
            },
            'exceptions': {
                'exact': {
                    'FAILED_ORDER_WITH_OPEN_ORDERS': InsufficientFunds,
                    'FAILED_LIMIT_ORDER': InvalidOrder,
                    'FAILED_MARKET_ORDER': InvalidOrder,
                },
            },
            'precisionMode': TICK_SIZE,
        })

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for btcturk
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = await self.publicGetServerExchangeinfo(params)
        #
        #    {
        #        "data": {
        #            "timeZone": "UTC",
        #            "serverTime": "1618826678404",
        #            "symbols": [
        #                {
        #                    "id": "1",
        #                    "name": "BTCTRY",
        #                    "nameNormalized": "BTC_TRY",
        #                    "status": "TRADING",
        #                    "numerator": "BTC",
        #                    "denominator": "TRY",
        #                    "numeratorScale": "8",
        #                    "denominatorScale": "2",
        #                    "hasFraction": False,
        #                    "filters": [
        #                        {
        #                            "filterType": "PRICE_FILTER",
        #                            "minPrice": "0.0000000000001",
        #                            "maxPrice": "10000000",
        #                            "tickSize": "10",
        #                            "minExchangeValue": "99.91",
        #                            "minAmount": null,
        #                            "maxAmount": null
        #                        }
        #                    ],
        #                    "orderMethods": [
        #                        "MARKET",
        #                        "LIMIT",
        #                        "STOP_MARKET",
        #                        "STOP_LIMIT"
        #                    ],
        #                    "displayFormat": "#,###",
        #                    "commissionFromNumerator": False,
        #                    "order": "1000",
        #                    "priceRounding": False
        #                },
        #                ...
        #            },
        #        ],
        #    }
        #
        data = self.safe_value(response, 'data')
        markets = self.safe_value(data, 'symbols', [])
        result = []
        for i in range(0, len(markets)):
            entry = markets[i]
            id = self.safe_string(entry, 'name')
            baseId = self.safe_string(entry, 'numerator')
            quoteId = self.safe_string(entry, 'denominator')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            filters = self.safe_value(entry, 'filters', [])
            minPrice = None
            maxPrice = None
            minAmount = None
            maxAmount = None
            minCost = None
            for j in range(0, len(filters)):
                filter = filters[j]
                filterType = self.safe_string(filter, 'filterType')
                if filterType == 'PRICE_FILTER':
                    minPrice = self.safe_number(filter, 'minPrice')
                    maxPrice = self.safe_number(filter, 'maxPrice')
                    minAmount = self.safe_number(filter, 'minAmount')
                    maxAmount = self.safe_number(filter, 'maxAmount')
                    minCost = self.safe_number(filter, 'minExchangeValue')
            status = self.safe_string(entry, 'status')
            result.append({
                'id': id,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': (status == 'TRADING'),
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.parse_number(self.parse_precision(self.safe_string(entry, 'numeratorScale'))),
                    'price': self.parse_number(self.parse_precision(self.safe_string(entry, 'denominatorScale'))),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': minAmount,
                        'max': maxAmount,
                    },
                    'price': {
                        'min': minPrice,
                        'max': maxPrice,
                    },
                    'cost': {
                        'min': minCost,
                        'max': None,
                    },
                },
                'info': entry,
            })
        return result

    def parse_balance(self, response):
        data = self.safe_value(response, 'data', [])
        result = {
            'info': response,
            'timestamp': None,
            'datetime': None,
        }
        for i in range(0, len(data)):
            entry = data[i]
            currencyId = self.safe_string(entry, 'asset')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_string(entry, 'balance')
            account['free'] = self.safe_string(entry, 'free')
            account['used'] = self.safe_string(entry, 'locked')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privateGetUsersBalances(params)
        #
        #     {
        #       "data": [
        #         {
        #           "asset": "TRY",
        #           "assetname": "Türk Lirası",
        #           "balance": "0",
        #           "locked": "0",
        #           "free": "0",
        #           "orderFund": "0",
        #           "requestFund": "0",
        #           "precision": 2
        #         }
        #       ]
        #     }
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairSymbol': market['id'],
        }
        response = await self.publicGetOrderbook(self.extend(request, params))
        #     {
        #       "data": {
        #         "timestamp": 1618827901241,
        #         "bids": [
        #           [
        #             "460263.00",
        #             "0.04244000"
        #           ]
        #         ]
        #       }
        #     }
        data = self.safe_value(response, 'data')
        timestamp = self.safe_integer(data, 'timestamp')
        return self.parse_order_book(data, market['symbol'], timestamp, 'bids', 'asks', 0, 1)

    def parse_ticker(self, ticker, market=None):
        #
        #   {
        #     "pair": "BTCTRY",
        #     "pairNormalized": "BTC_TRY",
        #     "timestamp": 1618826361234,
        #     "last": 462485,
        #     "high": 473976,
        #     "low": 444201,
        #     "bid": 461928,
        #     "ask": 462485,
        #     "open": 456915,
        #     "volume": 917.41368645,
        #     "average": 462868.29574589,
        #     "daily": 5570,
        #     "dailyPercent": 1.22,
        #     "denominatorSymbol": "TRY",
        #     "numeratorSymbol": "BTC",
        #     "order": 1000
        #   }
        #
        marketId = self.safe_string(ticker, 'pair')
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'timestamp')
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_string(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_string(ticker, 'daily'),
            'percentage': self.safe_string(ticker, 'dailyPercent'),
            'average': self.safe_string(ticker, 'average'),
            'baseVolume': self.safe_string(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        response = await self.publicGetTicker(params)
        tickers = self.safe_value(response, 'data')
        return self.parse_tickers(tickers, symbols)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        tickers = await self.fetch_tickers([symbol], params)
        return self.safe_value(tickers, symbol)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades
        #     {
        #       "pair": "BTCUSDT",
        #       "pairNormalized": "BTC_USDT",
        #       "numerator": "BTC",
        #       "denominator": "USDT",
        #       "date": "1618916879083",
        #       "tid": "637545136790672520",
        #       "price": "55774",
        #       "amount": "0.27917100",
        #       "side": "buy"
        #     }
        #
        # fetchMyTrades
        #     {
        #       "price": "56000",
        #       "numeratorSymbol": "BTC",
        #       "denominatorSymbol": "USDT",
        #       "orderType": "buy",
        #       "orderId": "2606935102",
        #       "id": "320874372",
        #       "timestamp": "1618916479593",
        #       "amount": "0.00020000",
        #       "fee": "0",
        #       "tax": "0"
        #     }
        #
        timestamp = self.safe_integer_2(trade, 'date', 'timestamp')
        id = self.safe_string_2(trade, 'tid', 'id')
        order = self.safe_string(trade, 'orderId')
        priceString = self.safe_string(trade, 'price')
        amountString = Precise.string_abs(self.safe_string(trade, 'amount'))
        marketId = self.safe_string(trade, 'pair')
        symbol = self.safe_symbol(marketId, market)
        side = self.safe_string_2(trade, 'side', 'orderType')
        fee = None
        feeAmountString = self.safe_string(trade, 'fee')
        if feeAmountString is not None:
            feeCurrency = self.safe_string(trade, 'denominatorSymbol')
            fee = {
                'cost': Precise.string_abs(feeAmountString),
                'currency': self.safe_currency_code(feeCurrency),
            }
        return self.safe_trade({
            'info': trade,
            'id': id,
            'order': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': fee,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        # maxCount = 50
        request = {
            'pairSymbol': market['id'],
        }
        if limit is not None:
            request['last'] = limit
        response = await self.publicGetTrades(self.extend(request, params))
        #
        #     {
        #       "data": [
        #         {
        #           "pair": "BTCTRY",
        #           "pairNormalized": "BTC_TRY",
        #           "numerator": "BTC",
        #           "denominator": "TRY",
        #           "date": 1618828421497,
        #           "tid": "637544252214980918",
        #           "price": "462585.00",
        #           "amount": "0.01618411",
        #           "side": "sell"
        #         }
        #       ]
        #     }
        #
        data = self.safe_value(response, 'data')
        return self.parse_trades(data, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #    {
        #        'timestamp': 1661990400,
        #        'high': 368388.0,
        #        'open': 368388.0,
        #        'low': 368388.0,
        #        'close': 368388.0,
        #        'volume': 0.00035208,
        #    }
        #
        return [
            self.safe_timestamp(ohlcv, 'timestamp'),
            self.safe_number(ohlcv, 'open'),
            self.safe_number(ohlcv, 'high'),
            self.safe_number(ohlcv, 'low'),
            self.safe_number(ohlcv, 'close'),
            self.safe_number(ohlcv, 'volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1h', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        see https://docs.btcturk.com/public-endpoints/get-kline-data
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the btcturk api endpoint
        :param int|None params['until']: timestamp in ms of the latest candle to fetch
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'resolution': self.safe_value(self.timeframes, timeframe, timeframe),  # allows the user to pass custom timeframes if needed
        }
        until = self.safe_integer(params, 'until', self.milliseconds())
        request['to'] = int(until / 1000)
        if since is not None:
            request['from'] = int(since / 1000)
        elif limit is None:  # since will also be None
            limit = 100  # default value
        if limit is not None:
            if timeframe == '1y':  # difficult with leap years
                raise BadRequest(self.id + ' fetchOHLCV() does not accept a limit parameter when timeframe == "1y"')
            seconds = self.parse_timeframe(timeframe)
            limitSeconds = seconds * (limit - 1)
            if since is not None:
                to = int(since / 1000) + limitSeconds
                request['to'] = min(request['to'], to)
            else:
                request['from'] = int(until / 1000) - limitSeconds
        response = await self.graphGetKlinesHistory(self.extend(request, params))
        #
        #    {
        #        "s": "ok",
        #        "t": [
        #          1661990400,
        #          1661990520,
        #          ...
        #        ],
        #        "h": [
        #          368388.0,
        #          369090.0,
        #          ...
        #        ],
        #        "o": [
        #          368388.0,
        #          368467.0,
        #          ...
        #        ],
        #        "l": [
        #          368388.0,
        #          368467.0,
        #          ...
        #        ],
        #        "c": [
        #          368388.0,
        #          369090.0,
        #          ...
        #        ],
        #        "v": [
        #          0.00035208,
        #          0.2972395,
        #          ...
        #        ]
        #    }
        #
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_ohlcvs(self, ohlcvs, market=None, timeframe='1m', since=None, limit=None):
        results = []
        timestamp = self.safe_value(ohlcvs, 't')
        high = self.safe_value(ohlcvs, 'h')
        open = self.safe_value(ohlcvs, 'o')
        low = self.safe_value(ohlcvs, 'l')
        close = self.safe_value(ohlcvs, 'c')
        volume = self.safe_value(ohlcvs, 'v')
        for i in range(0, len(timestamp)):
            ohlcv = {
                'timestamp': self.safe_value(timestamp, i),
                'high': self.safe_value(high, i),
                'open': self.safe_value(open, i),
                'low': self.safe_value(low, i),
                'close': self.safe_value(close, i),
                'volume': self.safe_value(volume, i),
            }
            results.append(self.parse_ohlcv(ohlcv, market))
        sorted = self.sort_by(results, 0)
        tail = (since is None)
        return self.filter_by_since_limit(sorted, since, limit, 0, tail)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'orderType': side,
            'orderMethod': type,
            'pairSymbol': market['id'],
            'quantity': self.amount_to_precision(symbol, amount),
        }
        if type != 'market':
            request['price'] = self.price_to_precision(symbol, price)
        if 'clientOrderId' in params:
            request['newClientOrderId'] = params['clientOrderId']
        elif not ('newClientOrderId' in params):
            request['newClientOrderId'] = self.uuid()
        response = await self.privatePostOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    async def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: not used by btcturk cancelOrder()
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        request = {
            'id': id,
        }
        return await self.privateDeleteOrder(self.extend(request, params))

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pairSymbol'] = market['id']
        response = await self.privateGetOpenOrders(self.extend(request, params))
        data = self.safe_value(response, 'data')
        bids = self.safe_value(data, 'bids', [])
        asks = self.safe_value(data, 'asks', [])
        return self.parse_orders(self.array_concat(bids, asks), market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairSymbol': market['id'],
        }
        if limit is not None:
            # default 100 max 1000
            request['last'] = limit
        if since is not None:
            request['startTime'] = int(math.floor(since / 1000))
        response = await self.privateGetAllOrders(self.extend(request, params))
        # {
        #   "data": [
        #     {
        #       "id": "2606012912",
        #       "price": "55000",
        #       "amount": "0.0003",
        #       "quantity": "0.0003",
        #       "stopPrice": "0",
        #       "pairSymbol": "BTCUSDT",
        #       "pairSymbolNormalized": "BTC_USDT",
        #       "type": "buy",
        #       "method": "limit",
        #       "orderClientId": "2ed187bd-59a8-4875-a212-1b793963b85c",
        #       "time": "1618913189253",
        #       "updateTime": "1618913189253",
        #       "status": "Untouched",
        #       "leftAmount": "0.0003000000000000"
        #     }
        #   ]
        # }
        data = self.safe_value(response, 'data')
        return self.parse_orders(data, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'Untouched': 'open',
            'Partial': 'open',
            'Canceled': 'canceled',
            'Closed': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market):
        #
        # fetchOrders / fetchOpenOrders
        #     {
        #       "id": 2605984008,
        #       "price": "55000",
        #       "amount": "0.00050000",
        #       "quantity": "0.00050000",
        #       "stopPrice": "0",
        #       "pairSymbol": "BTCUSDT",
        #       "pairSymbolNormalized": "BTC_USDT",
        #       "type": "buy",
        #       "method": "limit",
        #       "orderClientId": "f479bdb6-0965-4f03-95b5-daeb7aa5a3a5",
        #       "time": 0,
        #       "updateTime": 1618913083543,
        #       "status": "Untouched",
        #       "leftAmount": "0.00050000"
        #     }
        #
        # createOrder
        #     {
        #       "id": "2606935102",
        #       "quantity": "0.0002",
        #       "price": "56000",
        #       "stopPrice": null,
        #       "newOrderClientId": "98e5c491-7ed9-462b-9666-93553180fb28",
        #       "type": "buy",
        #       "method": "limit",
        #       "pairSymbol": "BTCUSDT",
        #       "pairSymbolNormalized": "BTC_USDT",
        #       "datetime": "1618916479523"
        #     }
        #
        id = self.safe_string(order, 'id')
        price = self.safe_string(order, 'price')
        amountString = self.safe_string_2(order, 'amount', 'quantity')
        amount = Precise.string_abs(amountString)
        remaining = self.safe_string(order, 'leftAmount')
        marketId = self.safe_string(order, 'pairSymbol')
        symbol = self.safe_symbol(marketId, market)
        side = self.safe_string(order, 'type')
        type = self.safe_string(order, 'method')
        clientOrderId = self.safe_string(order, 'orderClientId')
        timestamp = self.safe_integer_2(order, 'updateTime', 'datetime')
        rawStatus = self.safe_string(order, 'status')
        status = self.parse_order_status(rawStatus)
        return self.safe_order({
            'info': order,
            'id': id,
            'price': price,
            'amount': amount,
            'remaining': remaining,
            'filled': None,
            'cost': None,
            'average': None,
            'status': status,
            'side': side,
            'type': type,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'fee': None,
        }, market)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the btcturk api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = await self.privateGetUsersTransactionsTrade()
        #
        #     {
        #       "data": [
        #         {
        #           "price": "56000",
        #           "numeratorSymbol": "BTC",
        #           "denominatorSymbol": "USDT",
        #           "orderType": "buy",
        #           "orderId": "2606935102",
        #           "id": "320874372",
        #           "timestamp": "1618916479593",
        #           "amount": "0.00020000",
        #           "fee": "0",
        #           "tax": "0"
        #         }
        #       ],
        #       "success": True,
        #       "message": "SUCCESS",
        #       "code": "0"
        #     }
        #
        data = self.safe_value(response, 'data')
        return self.parse_trades(data, market, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if self.id == 'btctrader':
            raise ExchangeError(self.id + ' is an abstract base API for BTCExchange, BTCTurk')
        url = self.urls['api'][api] + '/' + path
        if (method == 'GET') or (method == 'DELETE'):
            if params:
                url += '?' + self.urlencode(params)
        else:
            body = self.json(params)
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            secret = self.base64_to_binary(self.secret)
            auth = self.apiKey + nonce
            headers = {
                'X-PCK': self.apiKey,
                'X-Stamp': nonce,
                'X-Signature': self.hmac(self.encode(auth), secret, hashlib.sha256, 'base64'),
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        errorCode = self.safe_string(response, 'code', '0')
        message = self.safe_string(response, 'message')
        output = body if (message is None) else message
        self.throw_exactly_matched_exception(self.exceptions['exact'], message, self.id + ' ' + output)
        if (errorCode != '0') and (errorCode != 'SUCCESS'):
            raise ExchangeError(self.id + ' ' + output)
