import pandas as pd 
import talib as ta


class calc_TA_data:

    def __init__(self, type1):
        self.type = type1

    def gen_ta(self, paired_stock):

        macd, macdsignal, macdhisto = ta.MACD(paired_stock['4. close'], fastperiod=12, slowperiod=26, signalperiod=9)
        rsi_trend = ta.RSI(paired_stock['4. close'],14)
        adx = ta.ADX(paired_stock['2. high'],paired_stock['3. low'],paired_stock['4. close'], timeperiod = 14)
        adxr = ta.ADXR(paired_stock['2. high'],paired_stock['3. low'],paired_stock['4. close'], timeperiod = 14)
        apo = ta.APO(paired_stock['4. close'], fastperiod=12, slowperiod=26, matype=0)
        aroonosc = ta.AROONOSC(paired_stock['2. high'],paired_stock['3. low'], timeperiod=14)
        bop = ta.BOP(paired_stock['1. open'], paired_stock['2. high'],paired_stock['3. low'],paired_stock['4. close'])
        cci = ta.CCI(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        cmo = ta.CMO(paired_stock['4. close'], timeperiod=14)
        dx = ta.DX(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        mfi = ta.MFI(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], paired_stock['6. volume'], timeperiod=14)
        minus_di = ta.MINUS_DI(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        minus_dm = ta.MINUS_DM(paired_stock['2. high'], paired_stock['3. low'], timeperiod=14)
        mom = ta.MOM(paired_stock['4. close'], timeperiod=10)
        plus_di = ta.PLUS_DI(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        plus_dm = ta.PLUS_DM(paired_stock['2. high'], paired_stock['3. low'], timeperiod=14)
        ppo = ta.PPO(paired_stock['4. close'], fastperiod=12, slowperiod=26, matype=0)
        fastk, fastd = ta.STOCHF(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], fastk_period=5, fastd_period=3, fastd_matype=0)
        ultosc = ta.ULTOSC(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
        trix = ta.TRIX(paired_stock['4. close'], timeperiod=30)
        willr = ta.WILLR(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        obv = ta.OBV(paired_stock['4. close'], paired_stock['6. volume'])
        adosc = ta.ADOSC(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], paired_stock['6. volume'], fastperiod=3, slowperiod=10)
        natr = ta.NATR(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        tema5 = ta.TEMA(paired_stock['4. close'], timeperiod=5)
        tema10 = ta.TEMA(paired_stock['4. close'], timeperiod=10)
        tema20 = ta.TEMA(paired_stock['4. close'], timeperiod=20)
        tema50 = ta.TEMA(paired_stock['4. close'], timeperiod=50)
        tema100 = ta.TEMA(paired_stock['4. close'], timeperiod=100)
        tema200 = ta.TEMA(paired_stock['4. close'], timeperiod=200)
        sar = ta.SAR(paired_stock['2. high'], paired_stock['3. low'], acceleration=0, maximum=0)
        bbupper, bbmid, bblower = ta.BBANDS(paired_stock['4. close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        sma5 = ta.SMA(paired_stock['4. close'], timeperiod = 5)
        sma10 = ta.SMA(paired_stock['4. close'], timeperiod = 10)
        sma50 = ta.SMA(paired_stock['4. close'], timeperiod = 50)
        sma100 = ta.SMA(paired_stock['4. close'], timeperiod = 100)
        sma200 = ta.SMA(paired_stock['4. close'], timeperiod = 200)
        beta = ta.BETA(paired_stock['2. high'], paired_stock['3. low'], timeperiod=5)
        std = ta.STDDEV(paired_stock['4. close'], timeperiod=5, nbdev=1)
        var = ta.VAR(paired_stock['4. close'], timeperiod=5, nbdev=1)
        avgtru = ta.ATR(paired_stock['2. high'], paired_stock['3. low'], paired_stock['4. close'], timeperiod=14)
        

        stock = {"Open": paired_stock['1. open'], "High": paired_stock['2. high'], "Low": paired_stock['3. low'],
                "Close": paired_stock['4. close'], "Adjusted Close": paired_stock['5. adjusted close'],
                "Volume": paired_stock['6. volume'],"Dividend Amount": paired_stock['7. dividend amount'],
                "MACD": macd, "MACDSignal": macdsignal, "MACDHisto": macdhisto, 
                "RSI": rsi_trend, 'ADX': adx, 'ADXR': adxr, 'APO': apo, 'AroonOSC': aroonosc,
                "BOP": bop, 'CCI': cci, 'CMO': cmo, 'DX': dx, 'MFI': mfi, 'Minus_DI': minus_di,
                'Minus_DM': minus_dm, 'MOM': mom, 'Plus_Di': plus_di, 'Plus_DM': plus_dm,
                'PPO': ppo, 'STOCHK': fastk, 'STOCHD': fastd,"UltOSC": ultosc,"TRIX":trix,
                "WillR":willr,"OBV":obv,"AsOSC":adosc,"NATR":natr,"TEMA5":tema5,"TEMA10":tema10,
                "TEMA20":tema20,"TEMA50":tema50,"TEMA100":tema100,"TEMA200":tema200, "SAR":sar,"BBUpper":bbupper,
                "BBMid": bbmid,"BBLower":bblower,"SMA5":sma5,"SMA10":sma10,"SMA50":sma50,
                "SMA100":sma100,"SMA200":sma200,"Beta":beta,"STD":std,"Var":var, "AvgTR": avgtru}

        full_stock_data = pd.DataFrame(stock)

        return full_stock_data