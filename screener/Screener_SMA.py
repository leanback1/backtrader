#screener that filters out stocks that are trading two standard deviations below the average price over the prior 20 days.
import backtrader as bt


class Screener_SMA(bt.Analyzer):
    params = (('period',20), ('devfactor',2),)

    def start(self):
        self.bband = {data: bt.indicators.BollingerBands(data,
                period=self.params.period, devfactor=self.params.devfactor)
                for data in self.datas}

    def stop(self):
        self.rets['over'] = list()
        self.rets['under'] = list()

        for data, band in self.bband.items():
            node = data._name, data.close[0], round(band.lines.bot[0], 2)
            if data > band.lines.bot:
                self.rets['over'].append(node)
            else:
                self.rets['under'].append(node)