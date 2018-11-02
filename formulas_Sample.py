'''
Formulas for technical analysis in Python Pandas
'''
import numpy as np
import pandas as pd
import time

def moving_average(df, n):
    """Calculate the moving average for the given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    Source: https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py
    """
    MA = pd.Series(df['close'].rolling(n, min_periods=n).mean(), name='{}_SMA'.format(n))
    df = df.join(MA)
    return df

def exponential_moving_average(df, n):
    """
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    Source: https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py
    """
    EMA = pd.Series(df['close'].ewm(span=n, min_periods=n).mean(), name= '{}_EMA'.format(n))
    df = df.join(EMA)
    return df

def relative_strength_index(df, n):
    """Calculate Relative Strength Index(RSI) for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    Source: https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py
    """
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
    RSI = pd.Series(PosDI / (PosDI + NegDI), name='{}_RSI'.format(n))
    df = df.join(RSI)
    return df

def bbands(df, period = 20, num_of_std=2.0):
    """Utilize Bollinger bands to measure volatility
    
    :param df: pandas.DataFrame
    :param period: Period for BBands
    :param num_of_std: Number of standard deviations
    :return: pandas.DataFrame
    Source: https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py
    """

    rolling_mean = pd.Series(df['close'].rolling(period, min_periods=period).mean())
    rolling_stdv = pd.Series(df['close'].rolling(period, min_periods=period).std())
    upper = rolling_mean + rolling_stdv
    lower = rolling_mean - rolling_stdv

    B1 = pd.Series(upper, name='BBands_up_{}'.format(str(period)))
    df = df.join(B1)
    B2 = pd.Series(lower, name='BBands_low_{}'.format(str(period)))
    df = df.join(B2)
    return df