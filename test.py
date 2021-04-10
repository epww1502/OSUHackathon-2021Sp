import pyupbit
import numpy as np
import requests


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = "xoxb-1940285825253-1967173782768-HWISLuHvbFLXxaRKuUbpqkqX"
 
post_message(myToken,"#stock","여기서 말할거야")




# 전체 기간 (2013 ~ Current) 백테스팅 코드
df = pyupbit.get_ohlcv("BTC")

df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.5
# df['range_shift1'] = df['range'].shift(1)
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma5']

fee = 0.0032 # 수수료
df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)

# 거래일별로 기간수익률
df['hpr'] = df['ror'].cumprod()

# MDD(Maximum Draw Down)은 투자 기간 중에 포트폴리오의 전 고점에서 저점까지의 최대 누적 손실을 의미합니다. 
# dd = Drawdown
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100 

print(df.tail())

print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])

df.to_csv("btc_ma.csv")



# 특정 년도 백테스팅 코드 (e.g. 2020)
'''
def get_hpr(ticker):
    try:
        df = pybithumb.get_ohlcv(ticker)
        df = df['2020']

        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) * 0.5
        df['target'] = df['open'] + df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']

        fee = 0.0032
        df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
        return df['hpr'][-2]
    except:
        return 1

tickers = pybithumb.get_tickers()

hprs = []
for ticker in tickers:
    hpr = get_hpr(ticker)
    hprs.append((ticker, hpr))

sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
print(sorted_hprs[:5]) # 기간수익률이 높은 5개의 코인 정보를 화면에 출력
'''