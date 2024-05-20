def rma(x, window):
    """
    Calculate an Exponential Moving Average over a series `x` with a window `window`.
    """
    return x.ewm(span=window, adjust=False).mean()

def rsi(series, period=14):
    """
    Calculate Relative Strength Index (RSI) of a given Pandas series and period length.
    """
    delta = series.diff()  # Change between prices
    up = delta.clip(lower=0)  # Only keep the positive differences (price increases)
    down = -delta.clip(upper=0)  # Only keep the negative differences, make them positive
    
    # Calculate the Exponential Moving Average (RMA) for upward and downward changes
    gain = rma(up, period)
    loss = rma(down, period)
    
    rs = gain / loss  # Relative Strength
    rsi = 100 - (100 / (1 + rs))  # Relative Strength Index
    
    return rsi

def ema(x, window):
    """
    Calculate Exponential Moving Average (EMA) similar to the TradingView Pine Script version.
    """
    return x.ewm(alpha=(2/(window+1)), adjust=False).mean()

def sma(x, window):
    """
    Calculate Simple Moving Average (SMA) using pandas.
    """
    return x.rolling(window).mean()

def macd(x, fast_length, slow_length, is_sma = False):
    fast_ma = sma(x, fast_length) if is_sma else ema(x, fast_length)
    slow_ma = sma(x, slow_length) if is_sma else ema(x, slow_length)
        
    return fast_ma - slow_ma

def macd_signal(macd, window, is_sma=False):
    return sma(macd, window) if is_sma else ema(macd, window)

def bollinger_bands(x, window, mult=2):
    basis = sma(x, window)
    
    dev = mult * x.rolling(window).std()
    
    upper = basis + dev
    lower = basis - dev
    
    return basis, upper, lower

def stochastique(x, window):
    return 100 * (x - x.rolling(window).min()) / (x.rolling(window).max() - x.rolling(window).min())
    
def stochastique_signal(x, window):
    return x.rolling(window).mean()

def sen(x, window):
    return (x.rolling(window).max() + x.rolling(window).min()) / 2

def senko_span_A(tekan_sen, kujin_sen, shift):
    return ((tekan_sen + kujin_sen) / 2).shift(shift)

def senko_span_B(x, window, shift):
    return ((x.rolling(window).min() + x.rolling(window).max()) / 2).shift(shift)