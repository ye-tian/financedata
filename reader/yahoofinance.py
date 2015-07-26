__author__ = 'ye.tian'

# yahoo's hidden API:
# ref: https://greenido.wordpress.com/2009/12/22/yahoo-finance-hidden-api/

# python3

import urllib.request
import urllib.parse

'''
Parameter s:
symbol

from

Parameter f:
a	Ask
a2	Average Daily Volume
a5	Ask Size
b	Bid
b2	Ask (Real-time)
b3	Bid (Real-time)
b4	Book Value
b6	Bid Size
c	Change & Percent Change
c1	Change
c3	Commission
c6	Change (Real-time)
c8	After Hours Change (Real-time)
d	Dividend/Share
d1	Last Trade Date
d2	Trade Date
e	Earnings/Share
e1	Error Indication (returned for symbol changed / invalid)
e7	EPS Estimate Current Year
e8	EPS Estimate Next Year
e9	EPS Estimate Next Quarter
f6	Float Shares
g	Day’s Low
h	Day’s High
j	52-week Low
k	52-week High
g1	Holdings Gain Percent
g3	Annualized Gain
g4	Holdings Gain
g5	Holdings Gain Percent (Real-time)
g6	Holdings Gain (Real-time)
i	More Info
i5	Order Book (Real-time)
j1	Market Capitalization
j3	Market Cap (Real-time)
j4	EBITDA
j5	Change From 52-week Low
j6	Percent Change From 52-week Low
k1	Last Trade (Real-time) With Time
k2	Change Percent (Real-time)
k3	Last Trade Size
k4	Change From 52-week High
k5	Percebt Change From 52-week High
l	Last Trade (With Time)
l1	Last Trade (Price Only)
l2	High Limit
l3	Low Limit
m	Day’s Range
m2	Day’s Range (Real-time)
m3	50-day Moving Average
m4	200-day Moving Average
m5	Change From 200-day Moving Average
m6	Percent Change From 200-day Moving Average
m7	Change From 50-day Moving Average
m8	Percent Change From 50-day Moving Average
n	Name
n4	Notes
o	Open
p	Previous Close
p1	Price Paid
p2	Change in Percent
p5	Price/Sales
p6	Price/Book
q	Ex-Dividend Date
r	P/E Ratio
r1	Dividend Pay Date
r2	P/E Ratio (Real-time)
r5	PEG Ratio
r6	Price/EPS Estimate Current Year
r7	Price/EPS Estimate Next Year
s	Symbol
s1	Shares Owned
s7	Short Ratio
t1	Last Trade Time
t6	Trade Links
t7	Ticker Trend
t8	1 yr Target Price
v	Volume
v1	Holdings Value
v7	Holdings Value (Real-time)
w	52-week Range
w1	Day’s Value Change
w4	Day’s Value Change (Real-time)
x	Stock Exchange
y	Dividend Yield

(Useful) Parameters for historical data:
a   from month
b   from day
c   from year
d   to month
e   to day
f   to year
'''

class YahooFinance(object):

    # yf = YahooFinance(type=1)
    # yf = YahooFinance(type=2)
    # type = 1: quote
    # type = 2: historical table
    def __init__(self, type, **kwargs):
        self.type = type
        if type == 1:
            self.mainurl = 'http://finance.yahoo.com/d/quotes.csv?%s'
        elif type == 2:
            self.mainurl = 'http://ichart.finance.yahoo.com/table.csv?%s'

        if len(kwargs) != 0:
            self.params = kwargs
        else:
            self.params = {}

    # type = 1: yf.call(s='msft', f='snd')
    # type = 2: yf.call(s='msft', a='01', b='10', c='2010', d='01', e='20', f='2010')
    # type 2:
    # from a='01', b='10', c='2010',
    # to d='01', e='20', f='2010'
    def call(self,**kwargs):
        if len(kwargs) != 0:
            self.params = kwargs
        callurl = self.mainurl % urllib.parse.urlencode(self.params)
        stream = urllib.request.urlopen(callurl).read()
        return_value = stream.decode('utf-8')

        if self.type == 1:
            return [x  if x[0] != '"' and x[-1] != '"' else x[1:-1] for x in return_value.strip().split(',')]
        else:
            return self.listify_table(return_value.strip())

    # [(Date,Open,High,Low,Close,Volume,Adj Close)]
    def listify_table(self, table):
        table = table.strip().split('\n') if type(table) is not list else table
        t = []
        for row in table[1:]:
            t.append(row.split(','))
        return t


# test
# yf = YahooFinance(type=1)
# print (yf.call(s='msft', f='snd'))
# ['msft', 'Microsoft Corporation', '1.24']

# yf = YahooFinance(type=2)
# print (yf.call(s='msft', a='01', b='10', c='2010', d='01', e='20', f='2010'))
# [['2010-02-19', '28.790001', '28.92', '28.690001', '28.77', '44451800', '25.000169'], ['2010-02-18', '28.59', '29.030001', '28.51', '28.969999', '42856500', '25.173961'], ...

