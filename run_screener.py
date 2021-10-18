import datetime
import backtrader as bt
import pandas as pd
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from screener.Screener_SMA import Screener_SMA

def main():
  #Instantiate Cerebro engine
  cerebro = bt.Cerebro()

  #Add data to Cerebro
  instruments = ['BABA', 'FB', 'ARKK', 'ORK.OL']
  for ticker in instruments:
    dateToday = str(int(time.time()))    
    tmpDateOneYearAgo = datetime.now() - relativedelta(years=2)
    dateOneYearAgo = str(int(time.mktime(tmpDateOneYearAgo.timetuple())))
    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+ ticker + '?period1=' + dateOneYearAgo +'&period2='+ dateToday +'&interval=1d&events=history&includeAdjustedClose=true'
    df = pd.read_csv(url, index_col='Date',parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data) 

  #Add analyzer for screener
  cerebro.addanalyzer(Screener_SMA)
  cerebro.run(runonce=False, stdstats=False, writer=True)

if __name__ == '__main__':
  main()
    #Run Cerebro Engine
   