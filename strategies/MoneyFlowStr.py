import backtrader as bt
from indicators.MoneyFlowInd import MFI

class MoneyFlowStr(bt.Strategy):
  def __init__(self):
    self.myind1 = MFI(self.data)