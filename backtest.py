from utils import Position
import ta
import pandas as pd
import numpy as np


def backtest(data: pd.DataFrame, sl: float, tp: float,
             rsi_window: int, rsi_lower: int, rsi_upper: int, n_shares=40) -> float:
    data = data.copy()
    rsi = ta.momentum.RSIIndicator(data.Close, window=rsi_window)

    data["rsi"] = rsi.rsi()

    capital = 1_000_000

    active_positions = []
    COM = .25 / 100

    for i, row in data.iterrows():
        for position in active_positions.copy():
            if row.Close > position.price * (1 + tp):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)
            if row.Close < position.price * (1 - sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        if row.rsi < rsi_lower:
            if capital > row.Close * n_shares * (1 + COM):
                capital -= row.Close * n_shares * (1 + COM)
                active_positions.append(Position(ticker="AAPL", price=row.Close))

    for position in active_positions.copy():
        capital += row.Close * n_shares * (1 - COM)
        active_positions.remove(position)

    return capital
