import pandas as pd
import ta
from collections import namedtuple


def backtest_atx(data: pd.DataFrame, adx_window: int, n_shares=40) -> float:

    data = data.copy()
    adx = ta.trend.ADXIndicator(high=data.High, low=data.Low, close=data.Close, window=adx_window)
# Creo que los podemos quitar
    data['ADX'] = adx.adx()
    data['+DI'] = adx.adx_pos()
    data['-DI'] = adx.adx_neg()

    capital = 1_000_000
    active_positions = []
    COM = .25 / 100

    for i, row in data.iterrows():
        for position in active_positions.copy():
            if row.Close > position.price * (1+ tp):
                capital += row.Close * n_shares * (1-COM)
                active_positions.remove(position)
            if row.Close < position.price * (1-sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        if row.adx_pos() > row.adx_neg() and row.adx() > 25:
            if capital > row.Close * n_shares * (1 + COM):
                capital -= row.Close * n_shares * (1 + COM)
                active_positions.append(Position(ticker= "AAPL", price= row.Close))

# PSAR
def backtest_psar(data: pd.DataFrame, step:float, max_step:float, n_shares=40) -> float:

    data = data.copy()
    psar = ta.trend.PSARIndicator(high=data.High, low=data.Low, close=data.Close, step=step, max_step=max_step)


    capital = 1_000_000
    active_positions = []
    COM = .25 / 100

    for i, row in data.iterrows():
        for position in active_positions.copy():
            if row.Close > position.price * (1+ tp):
                capital += row.Close * n_shares * (1-COM)
                active_positions.remove(position)
            if row.Close < position.price * (1-sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        if row.Close > row.psar.psar():
            if capital > row.Close * n_shares * (1 + COM):
                capital -= row.Close * n_shares * (1 + COM)
                active_positions.append(Position(ticker= "AAPL", price= row.Close))





