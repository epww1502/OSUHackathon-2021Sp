import pyupbit # For Upbit
import time
import requests # For slack

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
 
slack = "xoxb-1940285825253-1967173782768-aWN7zF405rIpqnBG9PA4Syvr"
# post_message(slack,"#stock","Connected to Slack")

## Balance Checking
def balance_check():
    post_message(slack,"#stock","Current Balance: \n")
    for ticker in pyupbit.get_tickers() :
        balance = upbit.get_balance(ticker)
        print(ticker, “:”, balance)
        post_message(slack,"#stock", ticker + ":" + balance + " ")
        time.sleep(0.1)

    # Method 2
    '''
    balances = upbit.get_balances()
    for balance in balances:
        print(balance)
        post_message(slack,"#stock", balance)
    '''

    # Method 3
    '''
    balances = upbit.get_balances()
    for i in range(0,34):
        print(i, balances[i]['currency'], balances[i]['balance'])
        post_message(slack,"#stock", i + " " + balances[i]['currency'] + " " + balances[i]['balance'])
    '''

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

