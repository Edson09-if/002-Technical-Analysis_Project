from utils import Position
import ta
import pandas as pd
import numpy as np


def backtest1(data: pd.DataFrame, sl: float, tp: float,
             rsi_window: int, rsi_lower: int, rsi_upper: int, n_shares=40,
              macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9) -> float:
    data = data.copy()
    data = data[:5000]
    rsi = ta.momentum.RSIIndicator(data.Close, window=rsi_window)

    data["rsi"] = rsi.rsi()

    #MACD
    macd_indicator = ta.trend.MACD(close=data['Close'], window_slow=26, window_fast=12, window_sign=9)
    data['MACD'] = macd_indicator.macd()
    data['MACD_signal'] = macd_indicator.macd_signal()

    capital = 1_000_000

    active_positions = []
    COM = .25 / 100

    #Close positions
    for i, row in data.iterrows():
        for position in active_positions.copy():
            if row.Close > position.price * (1 + tp):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)
            if row.Close < position.price * (1 - sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        # RSI SELL
        if row.rsi < rsi_lower:
            if capital > row.Close * n_shares * (1 + COM):
                capital -= row.Close * n_shares * (1 + COM)
                active_positions.append(Position(ticker="AAPL", price=row.Close))
        #MACD BUY
        if row.MACD > row.MACD_signal and row.MACD > 0:
            if capital >= row['Close'] * (1 + COM):
                capital -= row['Close'] * (1 + COM)
                active_positions.append(Position(ticker="AAPL", price=row.Close))
        # MACD SELL
        if row.MACD < row.MACD_signal and row.MACD > 0:
            if capital >= row['Close'] * (1 + COM):
                capital -= row['Close'] * (1 + COM)
                active_positions.append(Position(ticker="AAPL", price=row.Close))
            elif capital < row['Close'] * (1 + COM):
                capital += row['Close'] * (1 + COM)
                #active_positions.append(Position(ticker="AAPL", price=row.Close))



    for position in active_positions.copy():
        capital += row.Close * n_shares * (1 - COM)
        active_positions.remove(position)

    return capital

#MACD
        macd_fast = trial.suggest_int("macd_fast", 10, 15)  # Ventana rápida
        macd_slow = trial.suggest_int("macd_slow", 20, 30)  # Ventana lenta
        macd_signal = trial.suggest_int("macd_signal", 5, 12)  # Ventana de la línea de señal
        final_cap = backtest1(data, sl, tp, rsi_window, rsi_lower, rsi_upper, n_shares, macd_fast, macd_slow,macd_signal)

