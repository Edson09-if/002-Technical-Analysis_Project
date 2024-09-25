def backtestN(indicators: list, data: pd.DataFrame, sl: float, tp: float,
              rsi_window: int, rsi_lower: int, rsi_upper: int,
              boll_wind: int, boll_wind_dev: int,
              window_slo_macd: int, window_fast_macd: int, win_sig_macd: int, n_shares=40) -> float:
    data = data.copy()

    capital = 1_000_000
    active_positions = []
    COM = .25 / 100

    # Calculate indicators
    if 'RSI' in indicators:
        # RSI
        rsi = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
        data["rsi"] = rsi.rsi()

    if 'BOLL' in indicators:
        # Boll
        bollinger = ta.volatility.BollingerBands(close=data.Close,
                                                 window=boll_wind,
                                                 window_dev=boll_wind_dev)

        data["BollingerL"] = bollinger.bollinger_lband_indicator()  # unica señal de trading
        data["BollingerH"] = bollinger.bollinger_hband_indicator()  # unica señal de trading

    if "MACD" in indicators:
        macd_indicator = ta.trend.MACD(close=data['Close'], window_slow=window_slo_macd,
                                       window_fast=window_fast_macd, window_sign=win_sig_macd)

        # Añadir las columnas MACD y línea de señal al DataFrame
        data['MACD'] = macd_indicator.macd()
        data['MACD_signal'] = macd_indicator.macd_signal()

    active_positions = []
    short_positions = []
    portfolio_value = [capital]
    initial_margin = 1.28
    maintenance_margin = 1.25
    equity = capital
    margin_calls = []
    margin_acc = 0

    for i, row in data.iterrows():
        # trading_signal = row['BollingerL']
        # trading_signal_short = row['BollingerH']
        if 'BOLL' in indicators:
            trading_signal = row['BollingerL']
            trading_signal_short = row['BollingerH']
        else:
            trading_signal = False
            trading_signal_short = False

        # if 'RSI' in indicators:
        # rsi = row.get('rsi', float('nan'))

        # Closing Long Position
        for position in active_positions.copy():
            if row.Close > position.price * (1 + tp):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)
            if row.Close < position.price * (1 - sl):
                capital += row.Close * n_shares * (1 - COM)
                active_positions.remove(position)

        # CLOSING RSI POSITION
        # if indi == "RSI":
        if "RSI" in indicators:
            if row.rsi < rsi_lower:
                if capital > row.Close * n_shares * (1 + COM):
                    capital -= row.Close * n_shares * (1 + COM)
                    active_positions.append(
                        Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

            elif row.rsi > rsi_upper:
                short_sell = row.Close * n_shares
                required_margin = short_sell * initial_margin
                if capital >= required_margin:
                    capital -= short_sell * (COM) + required_margin
                    margin_acc += required_margin
                    short_positions.append(
                        Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

        # if indi == "BOLL":
        if "BOLL" in indicators:
            # Long trade entry
            if trading_signal == True:
                cost = row.Close * n_shares * (1 + COM)
                if capital > cost and len(active_positions) < 100:
                    capital -= row.Close * n_shares * (1 + COM)
                    active_positions.append(
                        Position(ticker="APPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

            # Short trade entry
            elif trading_signal_short == True:
                short_sell = row.Close * n_shares
                required_margin = short_sell * initial_margin
                if capital >= required_margin:
                    capital -= short_sell * (COM) + required_margin
                    margin_acc += required_margin
                    short_positions.append(
                        Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

        if "MACD" in indicators:
            if row.MACD > row.MACD_signal:
                if capital > row.Close * n_shares * (1 + COM):
                    capital -= row.Close * (1 + COM)
                    active_positions.append(
                        Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

            elif row.MACD < row.MACD_signal:
                short_sell = row.Close * n_shares
                required_margin = short_sell * initial_margin
                if capital >= required_margin:
                    capital -= short_sell * (COM) + required_margin
                    margin_acc += required_margin
                    short_positions.append(
                        Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

                    # Portfolio value
        long = sum(
            [position.n_shares * row.Close for position in active_positions])  # Long value is based on last close price
        short = sum([position.n_shares * (position.price - row.Close) for position in
                     short_positions])  # Short value is based on initial sell price
        short_margin = sum([position.n_shares * row.Close for position in
                            short_positions])  # Short value is based on initial sell price
        equity = capital + long - short
        portfolio_value.append(equity)

    # Backtesting is done :
    for position in active_positions.copy():
        capital += row.Close * position.n_shares * (1 - COM)
        active_positions.remove(position)

    for position in short_positions.copy():
        capital += row.Close * position.n_shares * (1 - COM)
        short_positions.remove(position)

    return portfolio_value

#combo = ['MACD']
#ed = backtestN(combo, data, sl=0.02, tp=0.02, rsi_window=10, rsi_lower=15, rsi_upper=50,
                         boll_wind=20,boll_wind_dev=2,
                           window_slo_macd=25, window_fast_macd=12, win_sig_macd=9,n_shares=40)