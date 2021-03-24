import requests
from src.Config import Config
from src.another import functions

class IncomeStatement:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.__points = 0
        statements = self.get_statement('income-statement')
        self.__net_income = [statement['netIncome'] for statement in statements]
        self.__eval_gross_profit_margin(statements)
        self.__eval_SGA_expenses(statements)
        self.__eval_RD_expenses(statements)
        self.__eval_depreciation_expenses(statements)
        self.__eval_interest_expense(statements)
        self.__eval_net_income(statements)
        
    
    def __eval_gross_profit_margin(self, statements:list):
        # a company with a history of gross profit margins abvoe 40% is an early indication that the company has a DCA
        average_margin = self.__calculate_average(statements, 'grossProfit', 'revenue')
        if average_margin >= 40.00:
            print(f'[EXCELLENT] Gross Profit Margin is above 40% for the last five years at {average_margin}%') 
            self.__points += 1
        elif average_margin >= 30.00: 
            print(f'[GOOD] Gross Profit Margin is above 30% for the last five years at {average_margin}%')
            self.__points += 0.5
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
            self.__points += 1
        elif average_RD_expense <= 10.00:
            print(f'[GOOD] Research and development costs less than 10% of gross profits over past five years at {average_RD_expense}%')
            self.__points += 0.5
        else:
            print(f'[POOR] Research and development costs greatar than 10% of gross profits over past five years at {average_RD_expense}%')

    def __eval_depreciation_expenses(self, statements):
        # companies that have low depreciation and amoritzation expenses as a percentage of gross profit tend to have a DCA
        # Buffet does not mention a specific threshold so I went with 6% for the top tier and 10% for the middle tier
        average_depreciation_expense = self.__calculate_average(statements, 'depreciationAndAmortization')
        self.__print_summary('Depreciation and ammortization expenses', 6, 15, average_depreciation_expense)

    def __eval_interest_expense(self, statements):
        # Buffet indicates that companies with interest expenses less than 15% of operating income tend to have a DCA, the lower the better
        average_interest_expense = self.__calculate_average(statements, 'interestExpense', 'operatingIncome')
        self.__print_summary('Interest expenses', 15, 20, average_interest_expense)
        # print(self.__points)

    def __eval_net_income(self, statements):
        # Companies with net income greatar than 20% of total revenues tend to have a DCA
        # Companies with net income less than 10% of total revenues tend to be in an industry with lots of competetion
        # where a single company cannot have an advantage over the others
        average_net_income = self.__calculate_average(statements, 'netIncome', 'revenue')
        if average_net_income >= 20.00:
            print(f'[EXCELLENT] Net income is at or above 20% of total revenues for the last five years at {average_net_income}%') 
            self.__points += 1
        elif average_net_income >= 10.00: 
            print(f'[GOOD] Net income is at or above 10% of total revenues for the last five years at {average_net_income}%')
            self.__points += 0.5
        else: 
            print(f'[POOR] Net income is below 10% of total revenues for the last five years at {average_net_income}%')

        trend = self.__determine_trend(statements, 'netIncome')
        if trend == 'increasing': 
            self.__points += 1
            print('[EXCELLENT] Net income increasing every year for past five years')
        elif trend == 'decreasing': 
            self.__points -= 1
            print('[POOR] Net income decreasing every year for past five years')
    
    def __calculate_average(self, statements:list, entry:str, divisor_entry:str='grossProfit'):
        total = 0
        for statement in statements:
            if statement[divisor_entry] == 0: continue
            percent = statement[entry] / statement[divisor_entry] * 100
            total += percent
        return round(total / len(statements), 2)
    
    @staticmethod
    def __determine_trend(statements:list, entry:str):
        increasing = True; decreasing = True
        ups = 0; downs = 0 #if trend is not strictly up or down, ups and downs will track which there are more of
        # iterating backwards since statements are stored most recent to oldest
        i = len(statements) - 2
        while i - 1 >= 0:
            if statements[i][entry] < statements[i-1][entry]: 
                decreasing = False
                ups += 1
            else: 
                increasing = False
                downs += 1
            i -= 1

        if increasing: return 'increasing'
        elif decreasing: return 'decreasing'
        else: return ('sideways', ups if ups > downs else -downs)

    def __print_summary(self, entry:str, upper_threshold:int, lower_threshold:int, entry_average:float):
        if entry_average <= upper_threshold:
            print(f'[EXCELLENT] {entry} less than or equal to {upper_threshold}% of gross profits over past five years at {entry_average}%')
            self.__points += 1
        elif entry_average <= lower_threshold:
            print(f'[GOOD] {entry} less than or equal to {lower_threshold}% of gross profits over past five years at {entry_average}%')
            self.__points += 0.5
        else:
            print(f'[POOR] {entry} greater than {lower_threshold}% of gross profits over past five years at {entry_average}%')
    
    def get_statement(self, statment_type:str):
        response = requests.get(f'https://financialmodelingprep.com/api/v3/{statment_type}/{self.ticker}?limit=120&apikey={Config.KEY}')
        return response.json()

    @property
    def points(self):
        return self.__points
    
    @property
    def net_income(self):
        return self.__net_income
        