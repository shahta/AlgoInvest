import requests
from src.Config import Config
from termcolor import colored
from time import sleep

class TickerEval:
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.__points = 0
        # net income is used for a lot of calcs so declaring here for easy access
        self.__net_income = []

    def evaluate_income_statement(self):
        statements = self.__get_statement('income-statement')
        self.__eval_gross_profit_margin(statements)
        # sleep(0.5)
        self.__eval_SGA_expenses(statements)
        # sleep(0.5)
        self.__eval_RD_expenses(statements)
        # sleep(0.5)
        self.__eval_depreciation_expenses(statements)
        # sleep(0.5)
        self.__eval_interest_expense(statements)
        # sleep(0.5)
        self.__eval_net_income(statements)
        # sleep(0.5)
        
        
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

        # populating self.__net_income
        self.__net_income = [statement['netIncome'] for statement in statements]

    def evaluate_balance_sheet(self):
        statements = self.__get_statement('balance-sheet-statement')
        self.__eval_cash_assets(statements)
        self.__eval_inventory(statements)
        self.__eval_current_ratio(statements)
        self.__eval_goodwill_intangibles(statements)
        self.__eval_return_on_assets(statements)
        self.__eval_long_term_debt(statements)
        self.__eval_retained_earnings(statements)

    def __eval_cash_assets(self, statements):
        # Buffet mentions having a large cash pile is good, but does not provide a quantifiable amount
        # He does mention that companies with an up-trend in cash and cash equivalents and low debts are promising signs of a company with a DCA
        trend = self.__determine_trend(statements, 'cashAndCashEquivalents')
        if trend == 'increasing':
            self.__points += 1
            print('[EXCELLENT] Cash assets increasing every year for past five years')
        elif trend == 'decreasing': 
            self.__points -= 1
            print('[POOR] Cash assets declining every year for past five years')
        elif trend[0] == 'sideways': 
            if trend[1] >= 3: 
                self.__points += 0.5
                print('[GOOD] Cash assets increasing for majority of past five years')
            elif trend[1] <= -3:
                self.__points -= 0.5
                print('[OKAY] Cash assets decreasing for majority of past five years')
            else:
                print('[NEUTRAL] Cash assets have no major trend, stable')
        
    def __eval_inventory(self, statements):
        # Companies with increasing inventory indicates that there is demand for the product or service and is a sign of a company with a DCA
        no_inventory = 0
        for statement in statements:
            if not statement['inventory']: no_inventory += 1
        # Some companies do not have inventory, if thats the case, no need to evaluate this entry; else, check trend of inventory over five year period
        if no_inventory == len(statements): return
        trend = self.__determine_trend(statements, 'inventory')
        if trend == 'increasing':
            self.__points += 1
            print('[EXCELLENT] Inventory increasing every year for past five years')
        elif trend == 'decreasing': 
            self.__points -= 1
            print('[POOR] Inventory declining every year for past five years')
        elif trend[0] == 'sideways': 
            if trend[1] >= 3: 
                self.__points += 0.5
                print('[GOOD] Inventory increasing for majority of past five years')
            elif trend[1] <= -3:
                self.__points -= 0.5
                print('[OKAY] Inventory decreasing for majority of past five years')
            else:
                print('[NEUTRAL] Inventory has no major trend, stable')
    
    def __eval_current_ratio(self, statements):
        # current ratio indicates whether a company can pay off its current liabilities 
        # ratio above 1 indicates company is liquid and can pay off debts; Current Ratio = Current Assets / Current Liabilities
        current_ratio = round(self.__calculate_average(statements, 'totalCurrentAssets', 'totalCurrentLiabilities') / 100, 2)
        if current_ratio >= 1: 
            print(f'[EXCELLENT] Current ratio is above 1 at {current_ratio}, company is liquid and can pay off its short term debts and obligations')
        else:
            print(f'[NEUTRAL] Current ratio is below 1 at {current_ratio}, consult net earnings to check if company can pay off its short term debts and obligations using earning power')
    
    def __eval_goodwill_intangibles(self, statements):
        # when companies buy other companies at an excess of book value, the excess is stored under goodwill
        # if goodwill is increasing, the company is out buying other companies
        # intangibles are assets such as patents or copyrights that could provide a DCA
        trend = self.__determine_trend(statements, 'goodwillAndIntangibleAssets')
        if trend == 'increasing' or (trend[0] == 'sideways' and trend[1] >= 3):
            print('[GOOD] Intangibles and goodwill increasing, company is out buying other companies; check which companies, and if those companies also have a DCA')

    def __eval_return_on_assets(self, statements):
        # return on assets is a ratio of how efficiently company management is utilizing assets to generate income; traditionally, the higher the ratio the better
        # however, Buffet indicates that with a high ratio, the company must have low total assets;
        # this would make it easier for someone to raise enough money to compete with said company making its DCA non-durable
        # whereas companies with good earnings and large total assets have low return on assets 
        # but for that reason its also harder for others to break in to the industry since they have to raise enough total assets to match and compete with the company
        ratio = 0
        total_assets = 0
        for i in range(len(statements)):
            assets = statements[i]['totalAssets']
            # checking for divide by zero error
            if not assets: continue
            ratio += self.__net_income[i] / assets * 100
            total_assets += assets
        ratio = round(ratio / len(statements), 2)
        total_assets = round(total_assets / len(statements))
        if ratio < 0:
            print(f'[POOR] Company has a negative return on assets of {ratio}%')
        elif ratio <= 15:
            print(f'[GOOD] Company has a return on assets of {ratio}%, this low ratio may indicate high total assets which provide barrier to entry and enhance DCA; Total Assets: ${total_assets:,}')
        else:
            print(f'[GOOD] Company has a return on assets of {ratio}%, this high ratio may indicate low assets which increase ease of entry and diminish DCA; Total Assets: ${total_assets:,}')

    def __eval_long_term_debt(self, statements):
        # Buffet indicates that companies with a DCA have little to none long term debt
        # A good sign is if a company can pay off all its long term debt using its net earnings within 3-4 years, amazing companies can do it under 2
        average_years = 0
        debt_average = 0
        for i in range(len(statements)):
           debt = statements[i]['longTermDebt']
           years_to_pay_off = statements[i]['longTermDebt'] / self.__net_income[i]
           average_years += years_to_pay_off
           debt_average += debt
        average_years /= len(statements)
        debt_average = round(debt_average / len(statements))
        if average_years <= 3:
            self.__points += 1
            print(f'[EXCELLENT] No significant long term debt (${debt_average:,}), can be paid off within 3 years using current earnings',)
        elif average_years <= 7:
            self.__points += 0.5
            print(f'[GOOD] Some long term debt (${debt_average:,}), however, can be paid off within 7 years using current earnings')
        if average_years > 7:
            print(f'[POOR] There is signifcant long term debt (${debt_average:,}), cannot be paid of within 7 years using current earnings')
    
    def __eval_debt_equity_ratio(self, statements):
        pass

    def __eval_retained_earnings(self, statements):
        # one of the most crucial indicators of a company with a DCA
        # if the retained earnings pool is growing, the company is growing its net worth and will theoretically make us rich also
        trend = self.__determine_trend(statements, 'retainedEarnings')
        if trend == 'increasing':
            self.__points += 1
            print('[EXCELLENT] Retained earnings pool increasing over 5 year period')
        elif trend == 'decreasing':
            self.__points -= 1
            print('[POOR] Retained earnings pool decreasing over 5 year period')

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
    
    def evaluate_cashflow_statement(self):
        pass

    def __get_statement(self, statment_type:str):
        response = requests.get(f'https://financialmodelingprep.com/api/v3/{statment_type}/{self.ticker}?limit=120&apikey={Config.KEY}')
        return response.json()