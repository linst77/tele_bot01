import binanceApi.kline as BiApi
import yaml
from binance.client import Client
import msr.handler as Msr
import datetime
import pandas as pd
from operator import itemgetter
class Find_rise_one():

    def __init__ ( self):

        self.binance = BiApi.BinanceKlineApi()
        self.all_symbol = self.binance.Get_all_symnbols_cctx()

        self.all_up_down = []
        self.compare( )

    def compare( self):

        ### make list 100 by high volume
        self.all_symbol = sorted( self.all_symbol, key=lambda x: x[2])[-150:]

        for i in self.all_symbol:
            current_price = float( i[1])
            if current_price > 0:

                persantage =  round( current_price / 100, 10)
                c_ema7 = self.binance.Get_ema( symbol=i[0], interval="30m", length=7)
                c_ema25 = self.binance.Get_ema( symbol=i[0], interval="30m", length=25)
                c_ema99 = self.binance.Get_ema( symbol=i[0], interval="30m", length=99)

                pers_7 = round( (c_ema7 / persantage) - 100, 10)
                pers_25 = round( (c_ema25 / persantage) - 100, 10)
                pers_99 = round( (c_ema99 / persantage) - 100, 10)

                self.all_up_down.append( [i[0], current_price, c_ema7, c_ema25, c_ema99, pers_7, pers_25, pers_99])
            else:
                pass

    @property
    def high_to_low7(self):

        #data_frame = pd.DataFrame( sorted( self.all_up_down, key=lambda x: x[5]))

        #data_frame.columns = ['time', 'symbol', 'current', 'ema7', 'ema25', 'ema99', '7d', '25d', '99d']
        #data_frame.index = [pd.to_datetime(x, unit='ms').strftime('%Y-%m-%d %H:%M:%S') for x in data_frame.time]

        #return data_frame
        return sorted( self.all_up_down, key=lambda x: x[5])
    @property
    def high_to_low25(self):
        return sorted( self.all_up_down, key=lambda x: x[6])
    @property
    def high_to_low99(self):
        return sorted( self.all_up_down, key=lambda x: x[7])



