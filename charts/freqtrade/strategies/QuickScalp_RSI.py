from freqtrade.strategy import IStrategy
from technical.indicators import RSI, EMA
import freqtrade.vendor.qtpylib.indicators as qtpylib

class QuickScalp_RSI(IStrategy):
    timeframe = '5m'
    
    # Your exact parameters
    stake_amount = 10
    stoploss = -0.005  # -0.5% - very tight
    min_roi = {
        "0": 0.01,     # 1% profit target
    }
    
    # Hyperoptable parameters
    buy_rsi = 25       # Buy when oversold
    sell_rsi = 75      # Sell when overbought
    rsi_period = 14
    
    # Enable immediate re-entry
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = True
    ignore_buying_expired_candle_after = 30
    
    # Trading fees (adjust for your exchange)
    exchange_fee = 0.001
    
    def informative_pairs(self):
        return []
    
    def populate_indicators(self, dataframe, metadata):
        dataframe['rsi'] = RSI(dataframe, timeperiod=self.rsi_period)
        dataframe['ema20'] = EMA(dataframe, timeperiod=20)
        return dataframe
    
    def populate_entry_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['rsi'] < self.buy_rsi) &
                (dataframe['close'] > dataframe['ema20']) &  # Trend filter
                (dataframe['volume'] > 0)  # Ensure liquidity
            ),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['rsi'] > self.sell_rsi) |
                (qtpylib.crossed_above(dataframe['rsi'], 70))  # Fast exit
            ),
            'exit_long'] = 1
        return dataframe