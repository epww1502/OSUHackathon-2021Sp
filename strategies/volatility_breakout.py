import time
import datetime
import pyupbit
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file_))))

from api import api

def get_target_price(ticker):
    df = upbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_yesterday_ma5(ticker):
    df = upbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]


def buy_crypto_currency(ticker):
    krw = upbit.get_balance(ticker)[2] # "upbit" from api.py
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    buy_bit = upbit.buy_market_order(ticker, unit) # {'uuid': '0182cc61-d1a6-4827-9505-74f60a8b076c', 'side': 'bid', 'ord_type': 'price', 'price': '10000.0', 'state': ', 'remaining_fee': wait', 'market': 'KRW-BTC', 'created_at': '2021-02-08T11:05:47+09:00', 'volume': None, 'remaining_volume': None, 'reserved_fee': '5.0', 'remaining_fee': '5.0', 'paid_fee': '0.0', 'locked': '10005.0', 'executed_volume': '0.0', 'trades_count': 0}
    # post_message(slack,"#stock", "BUY " + buy_bit['market'] + " / Price: " + buy_bit['price'] + " / Time: " + buy_bit['created_at'])


def sell_crypto_currency(ticker):
    unit = upbit.get_balance(ticker)[0]
    sell_bit = upbit.sell_market_order(ticker, unit)
    # post_message(slack,"#stock", "SELL " + sell_bit['market'] + " / Price: " + sell_bit['price'] + " / Time: " + sell_bit['created_at'])

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")
ma5 = get_yesterday_ma5("BTC")

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10): 
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            sell_crypto_currency("BTC")

        current_price = pyupbit.get_current_price("BTC")
        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("BTC")
    except:
        print("Error Occured")        
    time.sleep(1)