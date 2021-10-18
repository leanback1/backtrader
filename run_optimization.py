import datetime
import backtrader as bt
from strategies.GoldenCross import *

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from strategies.MAcrossover import MAcrossover

def main():
  cerebro = bt.Cerebro(optreturn=False)

  #Set data parameters and add to Cerebro
  ticker = "TSLA" 
  dateToday = str(int(time.time()))    
  tmpDateOneYearAgo = datetime.now() - relativedelta(years=2)
  dateOneYearAgo = str(int(time.mktime(tmpDateOneYearAgo.timetuple())))
  url = 'https://query1.finance.yahoo.com/v7/finance/download/'+ ticker + '?period1=' + dateOneYearAgo +'&period2='+ dateToday +'&interval=1d&events=history&includeAdjustedClose=true'
  df = pd.read_csv(url, index_col='Date',parse_dates=True)
  data = bt.feeds.PandasData(dataname=df)
  cerebro.adddata(data)

  #Add strategy to Cerebro
  cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
  cerebro.optstrategy(MAcrossover, pfast=range(5, 20), pslow=range(50, 100))  

  #Default position size
  cerebro.addsizer(bt.sizers.SizerFix, stake=3)
  optimized_runs = cerebro.run()

  final_results_list = []
  for run in optimized_runs:
      for strategy in run:
          PnL = round(strategy.broker.get_value() - 10000,2)
          sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
          final_results_list.append([strategy.params.pfast, 
              strategy.params.pslow, PnL, sharpe['sharperatio']])

  sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
                            reverse=True)
  for line in sort_by_sharpe[:5]:
      print(line)

if __name__ == "__main__":
    main()