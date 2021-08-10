import math
import backtrader as bt
from ta.trend import ADXIndicator
from ta.trend import AroonIndicator

class AroonDMI(bt.Strategy):
    params = (('aroon', 10), ('dmi', 14), ('order_percentage', 0.05))

    def __init__(self):
        '''
        Create an dictionary of indicators so that we can dynamically add the
        indicators to the strategy using a loop. This mean the strategy will
        work with any numner of data feeds. 
        '''
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['aroonup'] = bt.indicators.AroonUp(self.data, period=self.params.aroon)
            self.inds[d]['aroondown'] = bt.indicators.AroonDown(self.data, period=self.params.aroon)
            self.inds[d]['DIMinus'] = bt.indicators.MinusDirectionalIndicator(self.data, period=self.params.dmi)
            self.inds[d]['DIPlus'] = bt.indicators.PlusDirectionalIndicator(self.data, period=self.params.dmi)
            #self.inds[d]['BarStrength'] = abs((self.data.open - self.data.close) / (self.data.high - self.data.low) * 100)

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            amount_to_invest = (self.params.order_percentage * self.broker.cash)
            self.size = math.floor(amount_to_invest / d.close)
            if not pos:  # no market / no orders
                if self.inds[d]['DIPlus'][0] < self.inds[d]['DIMinus'][0]:
                    if self.inds[d]['aroonup'][0] == 0:
                        if self.inds[d]['aroondown'][0] == 100:
                            #if self.inds[d]['BarStrength'][0] < 20:
                            self.buy(data=d, size=self.size)

            else:
                if self.inds[d]['DIPlus'][0] > self.inds[d]['DIMinus'][0]:
                    if self.inds[d]['aroonup'][0] == 100:
                        if self.inds[d]['aroondown'][0] == 0:
                            self.close(data=d)


    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print('{} {} Closed: PnL Gross {}, Net {}'.format(dt, trade.data._name, round(trade.pnl,2), round(trade.pnlcomm,2)))


'''                if self.inds[d]['DIPlus'][0] > self.inds[d]['DIMinus'][0]:
                    if self.inds[d]['aroonup'][0] == 100:
                        if self.inds[d]['aroondown'][0] == 0:'''

'''if self.data.close[0] < self.data.open[0]:
                    if self.data.close[-1] < self.data.open[-1]:
                        if self.data.close[-2] < self.data.open[-2]:'''


'''
# Potential solution for writing divide by 0 avoiding errors most efficiently
def bar_str_div(x,y):
            if y or x ==0: return 0
            return abs((x/y)* 100) 


self.inds[d]['BarStrength'] = bar_str_div(x=(self.data.open - self.data.close), y=(self.data.high - self.data.low))'''