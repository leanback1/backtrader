from indicators.DonchianChannels import DonchianChannels
import backtrader as bt

class DonchianChannelsStr(bt.Strategy):
  def __init__(self):
    self.myind = DonchianChannels()

  def next(self):
    if self.data[0] > self.myind.dch[0]:
      self.buy()
    elif self.data[0] < self.myind.dcl[0]:
      self.sell()