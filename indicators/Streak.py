import backtrader as bt


class Streak(bt.ind.PeriodN):
    '''
    Keeps a counter of the current upwards/downwards/neutral streak
    '''
    lines = ('streak',)
    params = dict(period=2)  # need prev/cur days (2) for comparisons

    curstreak = 0

    def next(self):
        d0, d1 = self.data[0], self.data[-1]

        if d0 > d1:
            self.l.streak[0] = self.curstreak = max(1, self.curstreak + 1)
        elif d0 < d1:
            self.l.streak[0] = self.curstreak = min(-1, self.curstreak - 1)
        else:
            self.l.streak[0] = self.curstreak = 0
