############################ API ##########################
import pyupbit
import time
import requests # For slack
import datetime

# Read connect key and secret key from upbit.txt (first line: connect key / second: secret key)
with open("upbit.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(key, secret)

 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)


# Slack API 필요!
slack = "xoxb-~~~~" # Should input slack info
post_message(slack,"#stock","Connected to Slack")

## Balance Checking
def balance_check():
    post_message(slack,"#stock","Current Balance: \n")
    for ticker in pyupbit.get_tickers() :
        balance = upbit.get_balance(ticker)
        print(ticker, ":", balance)
        post_message(slack,"#stock", ticker + ":" + balance + " ")
        time.sleep(0.1)

    # Method 2
    '''
    balances = bithumb.get_balances()
    for balance in balances:
        print(balance)
        post_message(slack,"#stock", balance)
    '''

    # Method 3
    '''
    balances = bithumb.get_balances()
    for i in range(0,34):
        print(i, balances[i]['currency'], balances[i]['balance'])
        post_message(slack,"#stock", i + " " + balances[i]['currency'] + " " + balances[i]['balance'])
    '''

balance_check()


## Buying cryptocurrency -- DO NOT RUN THIS CODE!!!!!!!!!!!!!
'''
ret = bithumb.buy_limit_order("KRW-XRP", 100, 20)
print(ret)
'''

## Selling cryptocurrency -- DO NOT RUN THIS CODE!!!!!!!!!!!!!
'''
ret = bithumb.sell_limit_order("KRW-XRP", 1000, 20)
print(ret)
'''

## Cancel Order
'''
ret = bithumb.cancel_order('cc52be46-1000-4126-aee7-9bfafb867682')
print(ret)
'''




######################### Volatility_breakout.py ##############################
################# 이 아래로 주석 처리하면 구매나 판매는 작동 안함!! ###############
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
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