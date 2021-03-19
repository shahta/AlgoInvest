import requests
from src.Config import Config
from time import sleep

class TickerEval:
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.points = 0

    def evaluate_income_statement(self):
        statements = self.__get_statement('income-statement')
        self.__eval_gross_profit_margin(statements)
        sleep(0.5)
        self.__eval_SGA_expenses(statements)
        sleep(0.5)
        self.__eval_RD_expenses(statements)
        sleep(0.5)
        self.__eval_depreciation_expenses(statements)
        sleep(0.5)
        self.__eval_interest_expense(statements)
        sleep(0.5)
        self.__eval_net_income(statements)
        
    def __eval_gross_profit_margin(self, statements:list):
        # a company with a history of gross profit margins abvoe 40% is an early indication that the company has a DCA
        average_margin = self.__calculate_average(statements, 'grossProfit', 'revenue')
        if average_margin >= 40.00:
            print(f'[EXCELLENT] Gross Profit Margin is above 40% for the last five years at {average_margin}%') 
            self.points += 1
        elif average_margin >= 30.00: 
            print(f'[GOOD] Gross Profit Margin is above 30% for the last five years at {average_margin}%')
            self.points += 0.5
        else: print(f'[POOR] Gross Profit Margin is below 30% for the last five years at {average_margin}%')

    def __eval_SGA_expenses(self, statements):
        # a company with SGA expenses as a percentage of gross profits consistently lower than 35% may have a DCA
        average_SGA_expense = self.__calculate_average(statements, 'generalAndAdministrativeExpenses')
        self.__print_summary('Sales and general admin expenses', 35, 50, average_SGA_expense)
    
    def __eval_RD_expenses(self, statements):
        # Buffet indicates that companies with little to none R&D expenses tend to have a DCA working in their favour
        # I have chosen a conservative 10% of gross profits as a middle ground for this entry on the income sheet
        average_RD_expense = self.__calculate_average(statements, 'researchAndDevelopmentExpenses')
        if average_RD_expense == 0.00:
            print('[EXCELLENT] No research and development costs over past five years')
            self.points += 1
        elif average_RD_expense <= 10.00:
            print(f'[GOOD] Research and development costs less than 10% of gross profits over past five years at {average_RD_expense}%')
            self.points += 0.5
        else:
            print(f'[POOR] Research and development costs greatar than 10% of gross profits over past five years at {average_RD_expense}%')

    def __eval_depreciation_expenses(self, statements):
        # companies that have low depreciation and amoritzation expenses as a percentage of gross profit tend to have a DCA
        # Buffet does not mention a specific threshold so I went with 6% for the top tier and 10% for the middle tier
        average_depreciation_expense = self.__calculate_average(statements, 'depreciationAndAmortization')
        self.__print_summary('Depreciation and ammortization expenses', 6, 10, average_depreciation_expense)

    def __eval_interest_expense(self, statements):
        # Buffet indicates that companies with interest expenses less than 15% of operating income tend to have a DCA, the lower the better
        average_interest_expense = self.__calculate_average(statements, 'interestExpense', 'operatingIncome')
        self.__print_summary('Interest expenses', 15, 20, average_interest_expense)
        # print(self.points)

    def __eval_net_income(self, statements):
        # Companies with net income greatar than 20% of total revenues tend to have a DCA
        # Companies with net income less than 10% of total revenues tend to be in an industry with lots of competetion
        # where a single company cannot have an advantage over the others
        average_net_income, trend = self.__calculate_average(statements, 'netIncome', 'revenue', True)
        if average_net_income >= 20.00:
            print(f'[EXCELLENT] Net income is at or above 20% of total revenues for the last five years at {average_net_income}%') 
            self.points += 1
        elif average_net_income >= 10.00: 
            print(f'[GOOD] Net income is at or above 10% of total revenues for the last five years at {average_net_income}%')
            self.points += 0.5
        else: 
            print(f'[POOR] Net income is below 10% of total revenues for the last five years at {average_net_income}%')
        if trend == 'increasing': self.points += 1
        if trend == 'decreasing': self.points -= 1
        

    def __calculate_average(self, statements:list, entry:str, divisor_entry:str='grossProfit', trend:bool=False):
        values = []
        for statement in statements:
            percent = statement[entry] / statement[divisor_entry] * 100
            values.append(percent)
        if trend:
            print(values)
            trend = self.__determine_trend(values)
            return (round(self.__average(values), 2), trend)
        return round(self.__average(values), 2)
    
    def __print_summary(self, entry:str, upper_threshold:int, lower_threshold:int, entry_average:float):
        if entry_average <= upper_threshold:
            print(f'[EXCELLENT] {entry} less than or equal to {upper_threshold}% of gross profits over past five years at {entry_average}%')
            self.points += 1
        elif entry_average <= lower_threshold:
            print(f'[GOOD] {entry} less than or equal to {lower_threshold}% of gross profits over past five years at {entry_average}%')
            self.points += 0.5
        else:
            print(f'[POOR] {entry} greater than {lower_threshold}% of gross profits over past five years at {entry_average}%')
    
    def __determine_trend(self, prices:list):
        increasing = True; decreasing = True
        i = 0
        while i + 1 < len(prices):
            if prices[i] < prices[i+1]: decreasing = False
            else: increasing = False
            i += 1
        if increasing: return 'increasing'
        elif decreasing: return 'decreasing'
        else: return 'sideways'

    @staticmethod
    def __average(values:list):
        return sum(values) / len(values)
        
    
    def evaluate_balance_sheet(self):
        pass

    def evaluate_cashflow_statement(self):
        pass

    def __get_statement(self, statment_type:str):
        response = requests.get(f'https://financialmodelingprep.com/api/v3/{statment_type}/{self.ticker}?limit=120&apikey={Config.KEY}')
        return response.json()