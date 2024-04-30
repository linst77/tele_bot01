from binance.client import Client
import re
import pprint
import binanceApi.kline as BiApi
import time
import msr.handler as MS
import jf_api.find_symbol as japi
import ccxt
import asyncio

def ema_indicator799( ema7, ema99):
    if ema7 >= ema99:
        status = True
    if ema99 > ema7:
        status = False
    return status
def ema_indicator725( ema7, ema25):
    if ema7 >= ema25:
        status = True
    if ema25 > ema7:
        status = False
    return status


import ccxt

def high_raise_symbol( ):
    ppp = japi.Find_rise_one()

    high_7 = []
    high_25 = []
    high_99 = []

    for i in ppp.high_to_low7[:5]:
        high_7.append ( i[0])

    for j in ppp.high_to_low25[:5]:
        high_25.append ( j[0])

    for x in ppp.high_to_low99[:5]:
        high_99.append( x[0])

    return (high_7, high_25, high_99)

def run( ):

    BiApis = BiApi.BinanceKlineApi()
    client = BiApis.get_client
    msr = MS.MsrBot()

    count = 0
    cross7_99 = True
    cross7_25 = False

    while True:
        ema7 = BiApis.Get_ema('BTCUSDT', '30m', 7)
        ema25 = BiApis.Get_ema('BTCUSDT', '30m', 25)
        ema99 = BiApis.Get_ema('BTCUSDT', '30m', 99)
        ema150 = BiApis.Get_ema('BTCUSDT', '30m', 150)


        #pema7 = BiApis.Get_past_ema('BTCUSDT', '30m', date=(2024, 4,21), length=7)
        #pema25 = BiApis.Get_past_ema('BTCUSDT', '30m', date=(2024, 4,21), length=25)
        #pema99 = BiApis.Get_past_ema('BTCUSDT', '30m', date=(2024, 4,21), length=99)
        #pema150 = BiApis.Get_past_ema('BTCUSDT', '30m', date=(2024, 4,21), length=150)

        status7_25 = ema_indicator725( ema7, ema25)
        status7_99 = ema_indicator799( ema7, ema99)

        # message = buy_sell( status7_25, status7_99, client)


        # golden cross or death cross 7ma 99ma
        if status7_99 != cross7_99:
            if status7_99 == True:
                msr.send_message("BTC Golden Cross 7ma, 99ma")
                cross7_99 = status7_99
            else:
                msr.send_message("BTC Death Cross 7ma, 99ma --- Must Sell ---")
                cross7_99 = status7_99


        # golden cross or death cross 7ma 99ma
        if status7_25 != cross7_25:
            if status7_25 == True:
                msr.send_message("BTC Golden Cross 7ma, 25ma")
                cross7_25 = status7_25
            else:
                msr.send_message("BTC Death Cross 7ma, 25ma")
                cross7_25 = status7_25

        # 20 min to send raised symbol
        if count % 30 == 0:

            # most raised symbol
            d7, d25, d99 = high_raise_symbol()
            msr.send_message( "---30분 Symbol 정보---")
            msr.send_message( "현가격이 7일선 높믄종목 - " + str( d7))
            msr.send_message( "현가격이 25일선 높은정목 - " + str( d25))

        count += 1
        del( ema7, ema25, ema99, ema150)
        #print ( count)
        time.sleep( 1 * 60)

if __name__ == "__main__":
   run()
