import os, sys, argparse
import pandas as pd
import backtrader as bt
import datetime
from strategies.GoldenCross import GoldenCross
from strategies.AroonDMI import AroonDMI

cerebro = bt.Cerebro()

cerebro.broker.set_cash(40000)

datalist = []
for filename in os.listdir('insertpathhere'):
    symbol = filename.split(".")[0]
    path = 'insertpathhere/{}'.format(filename)
    datalist.append([path, symbol])


for i in range(len(datalist)):
    data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
    cerebro.adddata(data, name=datalist[i][1])
    

#cerebro.addsizer(bt.sizers.FixedSize, stake=1)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())


# Need to fix strategy class to work with multiple data feeds next
cerebro.addstrategy(AroonDMI) 

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#cerebro.plot()