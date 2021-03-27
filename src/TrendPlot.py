from matplotlib import pyplot as plt
import matplotlib



class TrendPlot:
    def __init__(self, plot_values:dict, company:str):
        self.__years = list(reversed(plot_values['years']))
        self.__net_income = list(reversed(plot_values['netIncome']))
        self.__total_assets = list(reversed(plot_values['totalAssets']))
        self.__long_term_debt = list(reversed(plot_values['longTermDebt']))
        self.__retained_earnings = list(reversed(plot_values['retainedEarnings']))
        self.company = company
    
    def plot(self):
        plt.plot(self.__years, self.__net_income, marker='.', markersize=12, label="Net Income" )
        plt.plot(self.__years, self.__total_assets, marker='.', markersize=12, label="Total Assets" )
        plt.plot(self.__years, self.__long_term_debt, marker='.', markersize=12, label="Long Term Debt" )
        plt.plot(self.__years, self.__retained_earnings, marker='.', markersize=12, label="Retained Earnings" )
        plt.xlabel('YEAR')
        plt.ylabel('US DOLLARS')
        plt.title(f"Key Metrics Trend Over {len(self.__years)} Year Duration for {self.company}")
        plt.legend()
        plt.grid()
        plt.minorticks_on()
        plt.show()
        self.__plt = plt
        

    def close(self):
        self.__plt.close()

        

