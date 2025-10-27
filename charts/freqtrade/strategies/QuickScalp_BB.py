from freqtrade.strategy import IStrategy
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta

class QuickScalp_BB(IStrategy):
    timeframe = '3m'  # Even shorter timeframe
    
    stake_amount = 10
    stoploss = -0.005
    min_roi = {"0": 0.01}
    
    # Bollinger Band settings
    bb_period = 20
    bb_dev = 2.0
    
    def populate_indicators(self, dataframe, metadata):
        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), 
            window=self.bb_period, 
            stds=self.bb_dev
        )
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_middle'] = bollinger['mid']
        dataframe['bb_upper'] = bollinger['upper']
        dataframe['bb_width'] = (dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_middle']
        
        return dataframe
    
    def populate_entry_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['bb_lower']) &  # Price below lower band
                (dataframe['bb_width'] > 0.02) &  # Ensure enough volatility
                (dataframe['volume'] > dataframe['volume'].rolling(20).mean())  # Volume spike
            ),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['bb_middle'])  # Exit at middle band
            ),
            'exit_long'] = 1
        return dataframe