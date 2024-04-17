import yaml
from binance.client import Client
import msr.handler as Msr
import datetime, re
import pandas as pd
import ccxt


class BinanceKlineApi():
    def __init__( self):
        self.msr_bot = Msr.MsrBot()
        self.api_key, self.secret = self.get_config( )

        # Binance
        self.client = Client( self.api_key, self.secret)
        self.symbol = 'BTSUSDT'

        # cctx
        self.ccxt_client = ccxt.binance(config={ 'apiKey': self.api_key, 'secret': self.secret, 'enableRateLimit': True })


    def Get_past_data(self, symbol, interval, date, length):
        # datetime convert
        target_day = datetime.date( date[0], date[1], date[2])
        past_day = target_day - datetime.timedelta( days=length)

        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=str( past_day),
                                              end_str=str( target_day), limit=200)
        return klines

    def Get_current_data( self, symbol, interval):
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=200)
        return klines

    def Get_current_price( self, symbol):
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def Get_past_price( self, symbol, date):
        past = self.client.get_historical_klines(symbol=symbol, interval="1d", start_str=str( date),
                                              end_str=None, limit=5)
        return past[0][4]

    # binance model
    def Get_all_tickers( self):
        all_ticker = self.client.get_all_tickers()
        return all_ticker

    # cctx model
    def Get_symbol_info( self, symbol):
        simbol = self.client.get_symbol_info( symbol)
        return simbol

    def Get_all_symbols( self):
        prices = self.client.get_all_tickers()
        all_symbols = []
        for i in prices:
            each = i.get('symbol')
            price = i.get( 'price')
            if "USDT" in each:
                all_symbols.append( [each, price])
        return all_symbols

    def Get_all_symnbols_cctx( self):
        tickers = self.ccxt_client.fetch_tickers()
        all_ticker = []

        for i in tickers:
            if i.endswith( 'USDT'):
                all_ticker.append( [
                                        tickers[i]['info']['symbol'],
                                        tickers[i]['info']['lastPrice'],
                                        tickers[i]['baseVolume']
                                    ])
        return all_ticker




    #########################################################################
    # indicator

    ### current ema ###
    def Get_ema(self, symbol, interval, length):

        if isinstance( interval, int):
            interval = str( interval) + "d"
        klines = self.Get_current_data( symbol=symbol, interval=interval)
        closes = [float(entry[4]) for entry in klines]
        return sum(closes[-length:]) / length

    ### past ema ###
    def Get_past_ema( self, symbol, interval, date, length):
        '''
        date: (yyyy, mm, dd)
        '''
        if isinstance( interval, int):
            interval = str( interval) + "d"

        klines = self.Get_past_data( symbol=symbol, interval=interval, date=date, length=length)
        closes = [float(entry[4]) for entry in klines]
        return sum(closes[-length:]) / length

    def get_config( self):

        with open( 'conf/binance.yaml') as f:
            deployment_def = yaml.load(f, Loader=yaml.FullLoader)

        return ( deployment_def['api_key'], deployment_def['secret'])

    @property
    def get_client(self):
        return self.client