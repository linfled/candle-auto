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

df = pyupbit.get_ohlcv("KRW-SAND", interval="minute5")    # 1시간봉 데이터 가져오기
print(df)    # 4시간봉 데이터 출력

ma5 = df['close'].rolling(window=7).mean()     # 종가 7일 이동평균선 변수 정하기
ma10 = df['close'].rolling(window=14).mean()    # 종가 14일 이동평균선 변수 정하기

last_ma5 = ma5[-2]     # 전 봉의 5일 이동평균선 데이터
last_ma10 = ma10[-2]    # 전 봉의 10일 이동평균선 데이터

print("======================================")
print(ma5[-2], "전봉의 7일 이동평균선")  #현재의 전봉 정보
print(ma10[-2], "전봉의 14일 이동평균선")
print("======================================")

while True:
    t1 = datetime.now()
    now = datetime.now()

    try:
        if last_ma5 > last_ma10:   # 매수   7일선이 14일선보다 위에 있을때
            print(ma5[-2], "7일 이동평균선")
            print(ma10[-2], "14일 이동평균선")
            print("7일선이 14일선보다 위에 있습니다")
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            krw = get_balance("KRW")       # 원화 잔고 조회
            print("현재 원화 잔고는", krw, "입니다")
            if krw > 1450000:
                upbit.buy_market_order("KRW-SAND", krw * 0.5)
                current_price = pyupbit.get_current_price("KRW-SAND")
                print("구매 완료")
                print(current_price, "현재가격")
                print("======================================")
                t5 = datetime.now()
                delta2 = t5 - t1
                time.sleep(60 - delta2.total_seconds())
                continue
            else:
                print("원화 잔고가 5000원보다 적습니다")
                print("======================================")
                t3 = datetime.now()
                delta2 = t3 - t1
                time.sleep(10 - delta2.total_seconds())
                continue

        if last_ma5 < last_ma10:  # 매도    7일선이 14일선보다 아래에 있을때
            print(ma5[-2], "7일 이동평균선")
            print(ma10[-2], "14일 이동평균선")
            print("7일선이 14일선보다 아래에 있습니다")
            print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분입니다 ")
            krw = get_balance("KRW")       # 원화 잔고 조회
            print("현재 원화 잔고는", krw, "입니다")
            btc = get_balance("KRW-SAND")       # BTC잔고 조회
            if btc != 0:
                upbit.sell_market_order("KRW-SANDC", btc)     # BTC잔고 전부 매도
                current_price = pyupbit.get_current_price("KRW-SAND")
                print("판매 완료")
                print(current_price, "현재가격")
                print("======================================")
            else:
                print("현재 가상화폐 잔고는", btc, "입니다")
                print("======================================")

            t4 = datetime.now()
            delta3 = t4 - t1
            time.sleep(10 - delta3.total_seconds())
            continue
        else:
            continue

    except Exception as e:
        print(e)

    t2 = datetime.now()
    delta = t2 - t1
    time.sleep(60 - delta.total_seconds())