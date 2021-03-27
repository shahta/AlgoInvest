from matplotlib import pyplot as plt



class TrendPlot:
    def __init__(self, plot_values:dict):
        self.__years = list(reversed(plot_values['years']))
        self.__net_income = list(reversed(plot_values['netIncome']))
        self.__total_assets = list(reversed(plot_values['totalAssets']))
        self.__long_term_debt = list(reversed(plot_values['longTermDebt']))
        self.__retained_earnings = list(reversed(plot_values['retainedEarnings']))
    
    def plot(self):
        plt.plot(self.__years, self.__net_income, label="Net Income" )
        plt.plot(self.__years, self.__total_assets, label="Total Assets" )
        plt.plot(self.__years, self.__long_term_debt, label="Long Term Debt" )
        plt.plot(self.__years, self.__retained_earnings, label="Retained Earnings" )
        plt.xlabel('YEAR')
        plt.ylabel('US DOLLARS')
        plt.title("Key Metrics Trend Over Five Year Duration")
        plt.legend()
        plt.show()


