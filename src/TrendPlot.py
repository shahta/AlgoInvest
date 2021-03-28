from matplotlib import pyplot as plt


class TrendPlot:
    def __init__(self, plot_values:dict, company:str):
        self.__years = list(reversed(plot_values['years']))
        self.__market_cap = list(reversed(plot_values['marketCap']))
        self.__pe_ratio = list(reversed(plot_values['PE']))
        self.__earnings_per_share = list(reversed(plot_values['EPS']))
        self.__dividend_yield = list(reversed(plot_values['dividendYield']))
        self.__current_ratio = list(reversed(plot_values['currentRatio']))
        self.__net_income = list(reversed(plot_values['netIncome']))
        self.__total_assets = list(reversed(plot_values['totalAssets']))
        self.__long_term_debt = list(reversed(plot_values['longTermDebt']))
        self.__retained_earnings = list(reversed(plot_values['retainedEarnings']))
        self.__stock_repurchased = list(reversed(plot_values['stockRepurchased']))
        self.company = company
    
    def plot_metrics(self):
        # plotting values
        plt.figure(1)
        plt.plot(self.__years, self.__net_income, marker='.', markersize=12, label="Net Income" )
        plt.plot(self.__years, self.__total_assets, marker='.', markersize=12, label="Total Assets" )
        # plt.plot(self.__years, self.__market_cap, marker='.', markersize=12, label="Market Cap" )
        plt.plot(self.__years, self.__long_term_debt, marker='.', markersize=12, label="Long Term Debt" )
        plt.plot(self.__years, self.__stock_repurchased, marker='.', markersize=12, label="Stock Repurchased" )
        plt.plot(self.__years, self.__retained_earnings, marker='.', markersize=12, label="Retained Earnings" )
        plt.xlabel('YEAR')
        plt.ylabel('US DOLLARS')
        plt.title(f"Key Metrics Trend Over {len(self.__years)} Year Duration for {self.company}")
        plt.legend()
        plt.grid()
        plt.minorticks_on()
        
        # plotting trends 
        plt.figure(2)
        plt.plot(self.__years, self.__earnings_per_share, marker='.', markersize=12, label="Earnings Per Share" )
        plt.plot(self.__years, self.__pe_ratio, marker='.', markersize=12, label="PE Ratio" )
        plt.plot(self.__years, self.__dividend_yield, marker='.', markersize=12, label="Dividend Yield" )
        plt.plot(self.__years, self.__current_ratio, marker='.', markersize=12, label="Current Ratio" )
        plt.xlabel('YEAR')
        plt.ylabel('MAGNITUDE')
        plt.title(f"Key Ratios Trend Over {len(self.__years)} Year Duration for {self.company}")
        plt.legend()
        plt.grid()
        plt.minorticks_on()
        plt.show()


        

