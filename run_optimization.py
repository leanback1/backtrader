import datetime
import backtrader as bt
from strategies.GoldenCross import *

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from strategies.MAcrossover import MAcrossover
from strategies.SmaCrossAdv import SmaCrossAdv


def get_data(ticker):
    df = None
    try:
        dateToday = str(int(time.time()))
        tmpDateOneYearAgo = datetime.now() - relativedelta(years=2)
        dateOneYearAgo = str(int(time.mktime(tmpDateOneYearAgo.timetuple())))
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + ticker + '?period1=' + \
            dateOneYearAgo + '&period2=' + dateToday + \
            '&interval=1d&events=history&includeAdjustedClose=true'
        df = pd.read_csv(url, index_col='Date', parse_dates=True)
    except Exception as e:  # proxy issues
        df = pd.read_csv('data/DNO.OL.csv', index_col='Date', parse_dates=True)
    return df


def main():
    cerebro = bt.Cerebro(optreturn=False)
    cerebro.adddata(bt.feeds.PandasData(dataname=get_data('EQNR.OL')))

    # Add strategy to Cerebro
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    #cerebro.optstrategy(MAcrossover, pfast=range(5, 20), pslow=range(50, 100))
    strats = cerebro.optstrategy(SmaCrossAdv, maperiod=range(10, 31))
    cerebro.broker.setcash(10000.0)
    # Default position size
    cerebro.addsizer(bt.sizers.SizerFix, stake=10)
    optimized_runs = cerebro.run(maxcpus=2)

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.get_value() - 10000, 2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            #final_results_list.append([strategy.params.pfast,strategy.params.pslow, PnL, sharpe['sharperatio']])
            final_results_list.append(
                [strategy.params.maperiod, PnL, sharpe['sharperatio']])

    sort_by_sharpe = sorted(
        final_results_list, key=lambda x: x[2], reverse=True)
    for line in sort_by_sharpe[:5]:
        print(line)


if __name__ == "__main__":
    main()
