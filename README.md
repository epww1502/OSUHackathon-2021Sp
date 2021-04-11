# OSUHackathon-2021Sp
OSUHackathon-2021Sp (Fintech)

## Proposal
Team: Kimchi
* Project: Automatic investment bot for cryptocurrency
* Proposal: During a busy day, invest in cryptocurrency and make a profit without getting an up close look every day! Based on Larry R. Williams' volatility breakout strategy, this program will buy and sell cryptocurrency automatically daily, and get a daily report via Slack!

## Install and configure project

### Install dependencies

```
pip install --no-cache-dir -r requirements.txt

```

## Useful Sources
* binance API: https://python-binance.readthedocs.io/en/latest/binance.html

* UPbit API: https://upbit.com/service_center/open_api_guide


## Upgrade list
* pip install pywinauto
* api.slack.com -> adding and setting a slack bot
* requests -> to use slack on python environmnet
* pyqt5-tools -> load gui designer for our app
```
pyqt5-tools designer
```

## How to run
make sure to install all dependencies before run our bot!
also, you should have your own api and secret keys
To get slack notification, put your slack api code on line 14 of 'auto_function.py' after set your slack channel
 
``` python main.py ```