import os
import sys
import argparse
from backtrader import indicator
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.MAcrossover import MAcrossover
from strategies.ATR import AverageTrueRange
from strategies.SmaCross import SmaCross
from strategies.DonchianChannelsStr import DonchianChannelsStr
from strategies.MoneyFlowStr import MoneyFlowStr
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

strategies = {
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold,
    "ma_cross": MAcrossover,
    "atr": AverageTrueRange,
    "sma": SmaCross,
    "donchian": DonchianChannelsStr,
    "mfi": MoneyFlowStr
}


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
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("strategy", help="Which strategy to run", type=str)
    args = parser.parse_args()

    if not args.strategy in strategies:
        print("Invalid strategy, must select one of {}".format(strategies.keys()))
        sys.exit()

    cerebro = Cerebro()
    cerebro.broker.setcash(250000)
    cerebro.addsizer(bt.sizers.AllInSizer, percents=90)
    # cerebro.addstrategy(MoneyFlowStr)
    cerebro.addstrategy(strategy=strategies[args.strategy])
    cerebro.adddata(bt.feeds.PandasData(dataname=get_data('EQNR.OL')))

    cerebro.addwriter(bt.WriterFile, csv=True, out='log.csv')
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()


if __name__ == "__main__":
    main()
