import pybithumb
import time


con_key = "81dd5f25e5daa70b2fff603901d2c09c" # Connect Key
sec_key = "82333efegeg9eg3e77c573weg34af17a" # Secret Key


bithumb = pybithumb.Bithumb(con_key, sec_key)



## Balance Checking
for ticker in pybithumb.get_tickers() :
    balance = bithumb.get_balance(ticker) # get balance of account
    print(ticker, “:”, balance)
    time.sleep(0.1)


## Buying cryptocurrency -- DO NOT RUN THIS CODE!!!!!!!!!!!!!
'''
krw = bithumb.get_balance("BTC")[2]
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/float(sell_price)

order = bithumb.buy_market_order("BTC", unit)
print(order)
'''

## Cancel Order
'''
time.sleep(10)
cancel = bithumb.cancel_order(order)
print(cancel)
'''

