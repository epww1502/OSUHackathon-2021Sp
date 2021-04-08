import pyupbit # For Upbit
import time


with open("upbit.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(key, secret)



## Balance Checking
print(upbit.get_balances())

## Buying cryptocurrency -- DO NOT RUN THIS CODE!!!!!!!!!!!!!
'''
ret = upbit.buy_limit_order("KRW-XRP", 100, 20)
print(ret)
'''

## Selling cryptocurrency -- DO NOT RUN THIS CODE!!!!!!!!!!!!!
'''
ret = upbit.sell_limit_order("KRW-XRP", 1000, 20)
print(ret)
'''

## Cancel Order
'''
ret = upbit.cancel_order('cc52be46-1000-4126-aee7-9bfafb867682')
print(ret)
'''

