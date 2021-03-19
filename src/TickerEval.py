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
        if average_SGA_expense <= 35.00:
            print(f'[EXCELLENT] Sales and general admin expenses less than or equal to 35% of gross profit for the last five years at {average_SGA_expense}%')
            self.points += 1
        elif average_SGA_expense <= 50.00:
            print(f'[GOOD] Sales and general admin expenses less than or equal to 50% of gross profit for the last five years at {average_SGA_expense}%')
            self.points += 0.5
        else:
            print(f'[POOR] Sales and general admin expenses greater than 50% of gross profit for the last five years at {average_SGA_expense}%')
    
    def __eval_RD_expenses(self, statements):
        # Buffet indicates that companies with little to none R&D expenses tend to have a DCA working in their favour
        # I have chosen a conservative 7% of gross profits as a threshold for the middle ground of this entry on the income sheet
        average_RD_expense = self.__calculate_average(statements, 'researchAndDevelopmentExpenses')
        if average_RD_expense == 0.00:
            print('[EXCELLENT] No research and development costs over past five years')
            self.points += 1
        elif average_RD_expense <= 7.00:
            print(f'[GOOD] Research and development costs less than 7% of gross profits over past five years at {average_RD_expense}%')
            self.points += 0.5
        else:
            print(f'[POOR] Research and development costs greatar than 7% of gross profits over past five years at {average_RD_expense}%')

    def __eval_depreciation_expenses(self, statements):
        # companies that have low depreciation and amoritzation expenses as a percentage of gross profit tend to have a DCA
        average_depreciation_expense = self.__calculate_average(statements, 'depreciationAndAmortization')
        if average_depreciation_expense <= 6.00:
            print(f'[EXCELLENT] Depreciation and ammortization expenses less than or equal to 6% of gross profits over past five years at {average_depreciation_expense}%')
            self.points += 1
        elif average_depreciation_expense <= 10.00:
            print(f'[GOOD] Depreciation and ammortization expenses less than or equal to 10% of gross profits over past five years at {average_depreciation_expense}%')
            self.points += 0.5
        else:
            print(f'[POOR] Depreciation and ammortization expenses greater than 10% of gross profits over past five years at {average_depreciation_expense}%')

    def __eval_interest_expense(self, statements):
        pass 
            
    def __calculate_average(self, statements:list, entry:str, divisor_entry:str='grossProfit'):
        values = []
        for statement in statements:
            percent = statement[entry] / statement[divisor_entry] * 100
            values.append(percent)
        return round(self.__average(values), 2)

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