import pandas as pd
from utils import optimize
from backtest import backtest
#from Backt_test import backtest1
import optuna

if __name__ == '__main__':
    #optimize()
    data = pd.read_csv("aapl_5m_train.csv").dropna()
    data = data[:5000]

    def optimize(trial):
        sl= trial.suggest_float("sl", 0.01, 0.15)
        tp = trial.suggest_float("tp", 0.01, 0.15)

        rsi_window = trial.suggest_float("rsi_window", 5, 50)
        rsi_lower = trial.suggest_float("rsi_lower", 10, 40)
        rsi_upper = trial.suggest_float("rsi_upper", 60, 90)

        n_shares = trial.suggest_float("n_shares", 40, 150)

        #MACD
        macd_fast = trial.suggest_int("macd_fast", 10, 15)  # Ventana rápida
        macd_slow = trial.suggest_int("macd_slow", 20, 30)  # Ventana lenta
        macd_signal = trial.suggest_int("macd_signal", 5, 12)  # Ventana de la línea de señal
        #final_cap = backtest1(data, sl, tp, rsi_window, rsi_lower, rsi_upper, n_shares, macd_fast, macd_slow,macd_signal)

        final_cap = backtest(data, sl, tp, rsi_window, rsi_lower, rsi_upper, n_shares)
        return final_cap

    study = optuna.create_study(direction="maximize")
    study.optimize(optimize, n_trials= 30)

