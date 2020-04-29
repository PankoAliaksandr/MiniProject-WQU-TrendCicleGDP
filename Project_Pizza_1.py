import statsmodels.api as sm
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt


class GDP:

    # Constructor
    def __init__(self):
        end_date = '2018-01-01'
        start_date = '1990-01-01'

        self.__gdp = pdr.DataReader('GDP', 'fred',
                                    start_date, end_date)

        # Hodrick-Prescott (HP) filter
        # A value of 1600 is suggested for quarterly data. We have quarterly.
        cycle, trend = sm.tsa.filters.hpfilter(self.__gdp, 1600)
        # GDP trend
        gdp_decomp = self.__gdp
        gdp_decomp["cycle"] = cycle
        gdp_decomp["trend"] = trend
        fig, ax = plt.subplots()

        gdp_decomp[["GDP", "trend"]].plot(ax=ax, fontsize=16)

        plt.show()

        # Cycles
        cycle.plot()

        # Christiano-Fitzgerald band-pass filter to estimate potential GDP
        cf_cycles, cf_trend = sm.tsa.filters.cffilter(self.__gdp, low=2,
                                                      high=6, drift=False)

        # GDP
        gdp_decomp1 = self.__gdp
        gdp_decomp1["cycle"] = cf_cycles
        gdp_decomp1["trend"] = cf_trend
        fig, ax1 = plt.subplots()

        gdp_decomp1[["GDP", "trend"]].plot(ax=ax1, fontsize=16)

        plt.show()

        cf_cycles.plot()

    def get_gdp(self):
        return self.__gdp


gdp = GDP()
result = gdp.get_gdp()
