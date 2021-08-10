import math
import backtrader as bt


class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ('order_percentage', 0.95))

    def __init__(self):
        '''
        Create an dictionary of indicators so that we can dynamically add the
        indicators to the strategy using a loop. This mean the strategy will
        work with any numner of data feeds. 
        '''
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['sma1'] = bt.indicators.SMA(d.close, period=self.params.fast)
            self.inds[d]['sma2'] = bt.indicators.SMA(d.close, period=self.params.slow)
            self.inds[d]['cross'] = bt.indicators.CrossOver(self.inds[d]['sma1'],self.inds[d]['sma2'])
            

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            amount_to_invest = (self.params.order_percentage * self.broker.cash)
            self.size = math.floor(amount_to_invest / d.close)
            if not pos:  # no market / no orders
                if self.inds[d]['cross'][0] == 1:
                    self.buy(data=d, size=self.size)
                elif self.inds[d]['cross'][0] == -1:
                    self.sell(data=d, size=self.size)
            else:
                if self.inds[d]['cross'][0] == 1:
                    self.close(data=d)
                    self.buy(data=d, size=self.size)
                elif self.inds[d]['cross'][0] == -1:
                    self.close(data=d)
                    self.sell(data=d, size=self.size)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print('{} {} Closed: PnL Gross {}, Net {}'.format(dt, trade.data._name, round(trade.pnl,2), round(trade.pnlcomm,2)))
