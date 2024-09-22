import ta
import pandas as pd
import numpy as np
import optuna
from typing import List

data = pd.read_csv("aapl_5m_train.csv").dropna()
data = data[:5000]
# Signal generation
def trad_strategies(strat: List[int], signal: str, rsi_bounds, boll_wind: int):
    rsi, boll, macd = strat

    if rsi:
        rsi_bound = rsi_bounds[0]

        rsi = ta.momentum.RSIIndicator(data.Close, window=rsi_bound)
        data["RSI"] = rsi.rsi()

    if boll:
        bollinger = ta.volatility.BollingerBands(close=data.Close,
                                                 window=boll_wind,
                                                 window_dev=2)

        data["BollingerL"] = bollinger.bollinger_lband_indicator()  # unica señal de trading
        data["BollingerH"] = bollinger.bollinger_hband_indicator()  # unica señal de trading

    if macd:
        macd_indicator = ta.trend.MACD(close=data['Close'], window_slow=26,
                                       window_fast=12, window_sign=9)

        # Añadir las columnas MACD y línea de señal al DataFrame
        data['MACD'] = macd_indicator.macd()
        data['MACD_signal'] = macd_indicator.macd_signal()

    data['Boll_Buy_Signal'] = 0
    data['MACD_Buy_Signal'] = 0
    data['RSI_Buy_Signal'] = 0
    data['Boll_Sell_Signal'] = 0
    data['MACD_Sell_Signal'] = 0
    data['RSI_Sell_Signal'] = 0

    if signal == "BUY":

        # Conditional por Boll
        data.loc[data['BollingerL'] == True, 'Boll_Buy_Signal'] = 1

        # MACD conditional
        data.loc[(data['MACD'] > data['MACD_signal']) & (data['MACD'] > 0), 'MACD_Buy_Signal'] = 1

        # RSI Conditional
        data.loc[data['RSI'] > 70, 'RSI_Buy_Signal'] = 1

    elif signal == "SELL":
        # Conditional por Boll
        data.loc[data['BollingerH'] == True, 'Boll_Sell_Signal'] = 1

        # MACD conditional
        data.loc[(data['MACD'] < data['MACD_signal']) & (data['MACD'] > 0), 'MACD_Sell_Signal'] = 1

        # RSI Conditional
        data.loc[data['RSI'] < 60, 'RSI_Sell_Signal'] = 1

    return data

strategy = [1,1,1]  # 1 RSI, 1 BOLL, 1 MACD
signal_type =  "BUY"
rsi_bounds= [14, 21]
boll_wind= 20

result_df = trad_strategies(strategy, signal_type,rsi_bounds, boll_wind )
print(result_df)