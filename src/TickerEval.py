import requests
from src.Config import Config

class TickerEval:
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.points = 0
    
    def evaluate_income_statement(self):
        statements = self.__get_statement('income-statement')
        # print(statements[0])
        self.__eval_gross_profit_margin(statements)
        self.__eval_SGA_expenses(statements)
        
    def __eval_gross_profit_margin(self, statements:list):
        # a company with a history of gross profit margins abvoe 40% is an early indication that the company has a DCA
        margins = []
        for statement in statements:
            margin = round(statement['grossProfit'] / statement['revenue'] * 100, 2)
            margins.append(margin)
        average_margin = round(sum(margins) / len(margins), 2)
        if average_margin >= 40.00:
            print(f'[EXCELLENT] Gross Profit Margin is above 40% for the last five years at {average_margin}%') 
            self.points += 1
        elif average_margin >= 30.00: 
            print(f'[GOOD] Gross Profit Margin is above 30% for the last five years at {average_margin}%')
            self.points += 0.5
        else: print(f'[POOR] Gross Profit Margin is below 30% for the last five years at {average_margin}%')

    def __eval_SGA_expenses(self, statements):
        pass

    
    def evaluate_balance_sheet(self):
        pass

    def evaluate_cashflow_statement(self):
        pass

    def __get_statement(self, statment_type:str):
        response = requests.get(f'https://financialmodelingprep.com/api/v3/{statment_type}/{self.ticker}?limit=120&apikey={Config.KEY}')
        return response.json()