import backtrader as bt

class DonchianChannels(bt.Indicator):
    alias = ('DCH', 'DonchianChannel')
    lines = ('dcm', 'dch', 'dcl')  # dc middle, dc high, dc low
    params = dict(period=20, lookback=-1 )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(dcm=dict(ls='--'), dch=dict(_samecolor=True), dcl=dict(_samecolor=True))

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        self.l.dcl = bt.ind.Lowest(lo, period=self.p.period)
        self.l.dcm = (self.l.dch + self.l.dcl) / 2.0  # avg of the above

'''
    Params Note:
      - `lookback` (default: -1)
        If `-1`, the bars to consider will start 1 bar in the past and the
        current high/low may break through the channel.
        If `0`, the current prices will be considered for the Donchian
        Channel. This means that the price will **NEVER** break through the
        upper/lower channel bands.
'''
