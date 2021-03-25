from src.TickerEval import TickerEval
from src.IncomeStatement import IncomeStatement
from termcolor import colored

class BalanceSheet:
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.ticker_eval = TickerEval(self.ticker)
        self.ticker_name = self.ticker_eval.get_company_name(self.ticker)
        self.income = IncomeStatement(self.ticker)
        self.__net_income = self.income.net_income
        self.__points = 0
        self.statements = self.ticker_eval.get_statement('balance-sheet-statement')
    
    
    def evaluate_balance_sheet(self):
        print(colored(f'-------------------------------EVALUATING BALANCE SHEETS FOR {self.ticker_name}-------------------------------------', 'green'))
        self.__eval_cash_assets(self.statements)
        self.__eval_inventory(self.statements)
        self.__eval_current_ratio(self.statements)
        self.__eval_goodwill_intangibles(self.statements)
        self.__eval_return_on_assets(self.statements)
        self.__eval_long_term_debt(self.statements)
        self.__eval_retained_earnings(self.statements)
    
    def __eval_cash_assets(self, statements):
        # Buffet mentions having a large cash pile is good, but does not provide a quantifiable amount
        # He does mention that companies with an up-trend in cash and cash equivalents and low debts are promising signs of a company with a DCA
        trend = self.ticker_eval.determine_trend(statements, 'cashAndCashEquivalents')
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
        trend = self.ticker_eval.determine_trend(statements, 'inventory')
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
        current_ratio = round(self.ticker_eval.calculate_average(statements, 'totalCurrentAssets', 'totalCurrentLiabilities') / 100, 2)
        if current_ratio >= 1: 
            print(f'[EXCELLENT] Current ratio is above 1 at {current_ratio}, company is liquid and can pay off its short term debts and obligations')
        else:
            print(f'[NEUTRAL] Current ratio is below 1 at {current_ratio}, consult net earnings to check if company can pay off its short term debts and obligations using earning power')
    
    def __eval_goodwill_intangibles(self, statements):
        # when companies buy other companies at an excess of book value, the excess is stored under goodwill
        # if goodwill is increasing, the company is out buying other companies
        # intangibles are assets such as patents or copyrights that could provide a DCA
        trend = self.ticker_eval.determine_trend(statements, 'goodwillAndIntangibleAssets')
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
        trend = self.ticker_eval.determine_trend(statements, 'retainedEarnings')
        if trend == 'increasing':
            self.__points += 1
            print('[EXCELLENT] Retained earnings pool increasing over 5 year period')
        elif trend == 'decreasing':
            self.__points -= 1
            print('[POOR] Retained earnings pool decreasing over 5 year period')
    
    @property
    def points(self):
        return self.__points