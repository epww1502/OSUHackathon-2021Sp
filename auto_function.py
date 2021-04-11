import time
import pyupbit
import requests # For slack

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)


# Slack API 필요!
slack = "yourslackcodehere" # Should input slack info
post_message(slack,"#stock","Connected to Slack")

def get_target(ticker):
    data_df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    #before = data_df.iloc[-2]

    current_open = data_df.iloc[0][0]
    max_before = data_df.iloc[0][1]
    min_before = data_df.iloc[0][2]
    target = current_open + (max_before - min_before) * 0.5
    print("target price:", target)
    return target

def get_five_days(ticker):
    data_df = pyupbit.get_ohlcv(ticker, interval="day", count=5)

    current_close = data_df['close']
    sum_current_close = 0
    five_days = current_close.rolling(5).mean()
    return five_days[-1]


def buy_crypto(ticker, upbit):
    try:
        kor_currency = upbit.get_balance(ticker="KRW")
        print(kor_currency)
        #orderbook = pyupbit.get_orderbook(ticker)
        #selling_price = orderbook['asks'][0]['price']   
        unit = kor_currency * 0.9995    # transaction fee = 0.05 %
        #if unit < 5000:
        #    unit = 5000
            
        print(unit, type(unit))
        buying_bit = upbit.buy_market_order(ticker, unit) # {'uuid': '0182cc61-d1a6-4827-9505-74f60a8b076c', 'side': 'bid', 'ord_type': 'price', 'price': '10000.0', 'state': ', 'remaining_fee': wait', 'market': 'KRW-BTC', 'created_at': '2021-02-08T11:05:47+09:00', 'volume': None, 'remaining_volume': None, 'reserved_fee': '5.0', 'remaining_fee': '5.0', 'paid_fee': '0.0', 'locked': '10005.0', 'executed_volume': '0.0', 'trades_count': 0}
        balance = upbit.get_balances()
        post_message(slack,"#stock", "BUY " + str(buying_bit['market']) + " / Price: " + str(buying_bit['price']) + " / Time(KOR): " + str(buying_bit['created_at']))
        for i in range(len(balance)):
            post_message(slack, "#stock", "[balance] " + str(balance[i]['currency']) +": " + str(balance[i]['balance']))
        return True
    except:
        print("can't buy!")
        return False

def sell_crypto(ticker, upbit):
    try:
        unit = upbit.get_balance(ticker=ticker)

        selling_bit = upbit.sell_market_order(ticker, unit)
        balance = upbit.get_balances()
        post_message(slack,"#stock", "[SELL] Crpyto: " + str(selling_bit['market']) + " / Price: " + str(selling_bit['price']) + " / Time(KOR): " + str(selling_bit['created_at']))
        for i in range(len(balance)):
            post_message(slack, "#stock", "[balance] " + str(balance[i]['currency']) +": " + str(balance[i]['balance']))
        return True
    except:
        print("can't sell!")
        return False
