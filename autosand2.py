import pyupbit
from datetime import datetime
import time

access_key = ""
secret_key = ""
upbit = pyupbit.Upbit(access_key, secret_key)  # 로그인


def get_balance(ticker):  # 잔고 조회 함수정의
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


krw = get_balance("KRW")  # 잔고조회
print("현재 원화 잔고는", krw, "입니다")

while True:
    t1 = datetime.now()
    now = datetime.now()

    df = pyupbit.get_ohlcv("KRW-SAND", interval="minute15")  # 1시간봉 데이터 가져오기

    ma5 = df['close'].rolling(window=10).mean()  # 종가 10일 이동평균선 변수 정하기
    ma10 = df['close'].rolling(window=20).mean()  # 종가 20일 이동평균선 변수 정하기

    close_data = df['close']  # 종가 데이터 변수 정하기
    open_data = df['open']  # 시가 데이터 변수 정하기

    last_ma5 = ma5[-2]  # 전 봉의 5일 이동평균선 데이터
    last_ma10 = ma10[-2]  # 전 봉의 10일 이동평균선 데이터

    current_price = pyupbit.get_current_price("KRW-SAND")
    print("**********************")
    print(current_price, "현재가격")
    print("데이터 가져옴")
    print("**********************")

    try:
        if last_ma5 < last_ma10 and close_data[-2] > last_ma10:
            print("5일선이 10일선보다 아래에 있고 현재가격이 10일선을 돌파했습니다")
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            krw = get_balance("KRW")
            print("현재 원화 잔고는", krw, "입니다")
            if krw > 1400000:
                upbit.buy_market_order("KRW-SAND", krw * 0.3)
                print("구매 완료")
                print(current_price, "구매가격")
                print("======================================")

        if last_ma5 > last_ma10 and close_data[-2] < last_ma5:
            btc = get_balance("SAND")
            print("현재 가상화폐 잔고는", btc, "입니다")
            upbit.sell_market_order("KRW-SAND", btc)
            print("판매 완료")
            print(current_price, "판매가격")
            print("======================================")

        else:
            print("======================================")
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            print("매매 타이밍이 아닙니다")
            t2 = datetime.now()
            delta2 = t2 - t1
            time.sleep(30 - delta2.total_seconds())
            continue

    except Exception as e:
        print(e)
