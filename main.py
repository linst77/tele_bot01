from binance.client import Client
import re
import pprint
import binanceApi.kline as BiApi
import time
import msr.handler as MS
import jf_api.find_symbol as japi
import ccxt
import asyncio

def buy_doge( client):
    usdtBalance = client.get_asset_balance(asset='USDT').get('free')
    if float( usdtBalance) > 5:
        order_buy = client.order_market_buy(symbol='DOGEUSDT', quoteOrderQty=usdtBalance)
        info = {
            "Symbol": str(order_buy['fills'][0]['commissionAsset']),
            "order_price": order_buy['fills'][0]['price'],
            "qty": order_buy['fills'][0]['qty'],
            "commission": order_buy['fills'][0]['commission'],
        }
        return info
    else:
        return "Stay"
def sell_doge( client):
    dogeBalance = client.get_asset_balance(asset='DOGE').get('free')
    if float( dogeBalance) > 5:
        order_buy = client.order_market_sell(symbol='DOGEUSDT', quantity=int(float(dogeBalance)))
        info = {
            "Symbol": str(order_buy['fills'][0]['commissionAsset']),
            "order_price": order_buy['fills'][0]['price'],
            "qty": order_buy['fills'][0]['qty'],
            "commission": order_buy['fills'][0]['commission'],
        }
        return info
    else:
        return "Stay"
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

def buy_sell( status725, status799, client):
    msr = MS.MsrBot()

    if status799 == True:
        msr.send_message("Golden")
        info = buy_doge( client)
        return info

    elif status799 == False:
        msr.send_message("Death")

        if status725 == True:
            info = buy_doge( client)
            return info
        else:
            info = sell_doge( client)
            return info




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
    status7_99 = None


    while True:
        ema7 = BiApis.Get_ema('DOGEUSDT', '30m', 7)
        ema25 = BiApis.Get_ema('DOGEUSDT', '30m', 25)
        ema99 = BiApis.Get_ema('DOGEUSDT', '30m', 99)

        status7_25 = ema_indicator725( ema7, ema25)
        status7_99 = ema_indicator799( ema7, ema99)

        message = buy_sell( status7_25, status7_99, client)

        msr.send_message( "ema7:" + str( ema7) + "ema25:" + str( ema25) + "ema99:" + str( ema99))
        msr.send_message( message)

        d7, d25, d99 = high_raise_symbol()
        msr.send_message( str( d7))
        msr.send_message( str( d25))
        msr.send_message( str( d99))

        time.sleep( 30 * 60)

if __name__ == "__main__":
   run()





