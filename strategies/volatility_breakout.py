import time
import datetime
import pyupbit

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
    upbit.buy_market_order(ticker, unit)


def sell_crypto_currency(ticker):
    unit = upbit.get_balance(ticker)[0]
    upbit.sell_market_order(ticker, unit)


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