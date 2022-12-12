
#
# Full Python Script
# for MonteCarlo Simulation of a
# specific market symbol.
#
# Josef Langerman
# October 2022
#

# Following the steps from https://www.investopedia.com/terms/m/montecarlosimulation.asp we will calculate a trajectory
# It is basically a brownian motion with drift.
# For more detail see: Xiang, Jeremy Ng Phak, Shubashini Rathina Velu, and Sotirios Zygiaris.
# "Monte Carlo Simulation Prediction of Stock Prices." 2021 14th International Conference on Developments in eSystems Engineering (DeSE). IEEE, 2021.
# https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9719349&casa_token=S_TwoD4b0KkAAAAA:1i_6iQCKDhgx1RHoy61d-YbDnnjyeH6K7OYghukRtrKutcbV4PXC5BIf9pv9Et6xbDNqsydVyGQ&tag=1

# Load dataframe with Share Price
# Used this query on alpha vantage: https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=VOO&apikey=YOURKEYGOESHERE&datatype=csv

# Todo
# * Add Github
# * Add Better Error Handling
# * Add Data Folder and DataScience Software Engineering Guideline
# * Add other markets
# * Add way to simulate different combinations of portfolios algorithmically
# * Get away from pandas. Rewrite CSV section. Can then use reverse function.
# * Add VaR
# * Do a code review

from math import e, log
from statistics import variance, stdev, mean
from numpy import percentile
import random
import matplotlib.pyplot as plt
import pandas as pd
NUM_WALKS = 10_000 


class Symbol(object):
    ''' Class to represent a timeseries of prices for  a specifc ticker
     symbol and some descriptive statistics.

    Attributes
    ===========
    symbol: str
    name: str
    prices: float
    periods: int # number of periods
    periodic_log_monthly_return :float
    stdev_logreturn: float

    Methods
    =======
    get_data:
        retrieves and prepares time_series data set
    set_parameters:
        calculates the mean, variance and standard deviation

    '''

    def __init__(self, symbol, name, fname):
        self.symbol = symbol
        self.name = name
        self.periods = 0
        self.prices = None
        self.log_monthly_returns = None
        self.stdev_logreturn = 0
        self.get_data(fname)
        self.set_log_monthly_returns()
        self.set_montecarlo_parameters()

    def get_data(self, fname):
        '''Load dataframe with Share Price.'''
        df = pd.read_csv("data/"+fname)
        reverseCloseSP500 = df['close'].array
        self.prices = reverseCloseSP500[::-1]
        self.periods = len(self.prices)

    def set_montecarlo_parameters(self):
        if self.prices is not None:
            # self.mean = mean(self.prices)
            # self.variance = variance(self.prices)
            # self.stdev = stdev(self.prices)
            self.drift = mean(self.log_monthly_returns) - \
                variance(self.log_monthly_returns)/2
            self.stdev_logreturn = stdev(self.log_monthly_returns)

    def set_log_monthly_returns(self):
        if self.prices is not None:
            self.log_monthly_returns = []
            for i in range(1, len(self.prices)):
                self.log_monthly_returns.append(log(self.prices[i] /
                                                self.prices[i-1]))


def randomWalk(periods, drift, stdev_logreturn, startPrice):
    ''' This is the main section where we run the simulation. '''
    forwardSeries = []
    forwardSeries.append(startPrice)
    for i in range(periods):
        shock = stdev_logreturn * random.normalvariate(0, 1)
        nextDayPrice = startPrice * (e**(drift+shock))
        startPrice = nextDayPrice
        forwardSeries.append(nextDayPrice)
    return forwardSeries


sp500 = Symbol("VOO", "S&P500", "monthly_adjusted_VOO.csv")


# Here we run the simulation
scenarios = []  # This will turn into a 2D list with all the scenarios
for i in range(0, NUM_WALKS):
    scenario = randomWalk(sp500.periods, sp500.drift,
                          sp500.stdev_logreturn, 54.15)
    plt.plot(scenario)
    scenarios.append(scenario)
    plt.title("monte-carlo simulation of stock price development")

plt.xlabel("Month")
plt.ylabel("stock price")
plt.show()

# Generate some descriptive statistics
total = 0
total2 = 0 
means = []
returns_overperiod = []
for i in range(0, NUM_WALKS):
    total2 += scenarios[i][-1] 
    total = total + mean(scenarios[i])
    means.append(mean(scenarios[i]))
    returns_overperiod.append(scenarios[i][-1] - scenarios[i][0])

print("The mean of ", NUM_WALKS, " walks is: ", total / NUM_WALKS)
print("The mean of final price of the SP 5000 of ", NUM_WALKS, " walks is: ", total2 / NUM_WALKS)
print(f"The mean return of the S&P 500 over {NUM_WALKS} walks is ",
      f"{mean(returns_overperiod)}")
print(f"The mean annual return of the S&P 500 over {NUM_WALKS} walks is ",
      f"{(mean(returns_overperiod)/sp500.periods)*12}")
