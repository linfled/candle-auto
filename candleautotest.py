import pyupbit
from datetime import datetime
import time

access_key = ""
secret_key = ""
upbit = pyupbit.Upbit(access_key, secret_key)    # 로그인

def get_balance(ticker):     # 잔고 조회 함수정의
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


krw = get_balance("KRW")     # 잔고조회
print("현재 원화 잔고는", krw, "입니다")

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")    # 1시간봉 데이터 가져오기
print(df)    # 1시간봉 데이터 출력

close_data = df['close']    # 종가 데이터 변수 정하기
open_data = df['open']     # 시가 데이터 변수 정하기
print(close_data[-2], "전 봉의 종가")    # 전 봉의 종가 출력


while True:
    t1 = datetime.now()
    now = datetime.now()
    current_price = pyupbit.get_current_price("KRW-BTC")  # 현재가 조회
    print(current_price, "현재가격")
    try:
        if open_data[-2] < close_data[-2] and current_price > close_data[-2] * 1.015:
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            krw = get_balance("KRW")       # 원화 잔고 조회
            print("현재 원화 잔고는", krw, "입니다")
            if krw > 1450000:
                upbit.buy_market_order("KRW-BTC", 10000)
                print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
                print("구매 완료")
                print(open_data[-2], "시가", close_data[-2], "종가", current_price, "현재가격")
                print("======================================")
            else:
                continue

        if open_data[-2] < close_data[-2] and current_price < close_data[-2] * 0.985:
            btc = get_balance("BTC")
            print("현재 가상화폐 잔고는", btc, "입니다")
            if btc != 0:
                upbit.sell_market_order("KRW-BTC", btc)     # BTC잔고 전부 매도
                print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
                print("판매 완료")
                print("======================================")
            else:
                continue

        else:
            print("======================================")
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            print("매수 타이밍이 아닙니다")
            t4 = datetime.now()
            delta2 = t4 - t1
            time.sleep(60 - delta2.total_seconds())
            continue

    except Exception as e:
        print(e)

    t5 = datetime.now()
    delta = t5 - t1
    time.sleep(60 - delta.total_seconds())