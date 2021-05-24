import requests
from src.Config import Config
from termcolor import colored


class TickerEval:
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.ticker_name = self.__get_company_name(self.ticker)
        self.__points = 0
        self.excellent = colored('[EXCELLENT]', 'green')
        self.good = colored('[GOOD]', 'blue')
        self.poor = colored('[POOR]', 'red')
        self.analysis = colored('[ANALYSIS]', 'yellow')

        # the following are used for plotting trends and other calcs
        self.__net_income = []
        self.__retained_earnings = []
        self.__total_assets = []
        self.__stock_repurchased = []
        self.__long_term_debt = []
        self.__market_cap = []
        self.__earnings_per_share = []
        self.__pe_ratio = []
        self.__dividend_yield = []
        self.__current_ratio = []
        self.__years = []

    @staticmethod
    def __calculate_average(statements:list, entry:str, divisor_entry:str='grossProfit'):
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
        # iterating backwards since statements are stored in reverse chronological order
        i = len(statements) - 1
        while i - 1 >= 0:
            if statements[i][entry] < statements[i-1][entry]: 
                decreasing = False
                ups += 1
            else: 
                increasing = False
                downs += 1
            i -= 1

        if increasing and decreasing: return 'stagnant'
        elif increasing: return 'increasing'
        elif decreasing: return 'decreasing'
        else: return ('sideways', ups if ups > downs else -downs)

    def __get_statement(self, statement_type:str):
        response = requests.get(f'https://financialmodelingprep.com/api/v3/{statement_type}/{self.ticker}?limit=120&apikey={Config.KEY}')
        return response.json()

    @staticmethod
    def __get_company_name(ticker:str):
        stocks = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={Config.KEY}').json()
        for stock in stocks:
            if stock['symbol'] == ticker: 
                return stock['name'].upper()
                
    def evaluate_income_statement(self):
        print(colored(f'-------------------------------EVALUATING INCOME STATEMENTS FOR {self.ticker_name}-------------------------------------', 'cyan'))
        statements = self.__get_statement('income-statement')
        self.__eval_gross_profit_margin(statements)
        self.__eval_SGA_expenses(statements)
        self.__eval_RD_expenses(statements)
        self.__eval_depreciation_expenses(statements)
        self.__eval_interest_expense(statements)
        self.__eval_net_income(statements)
        print(' ')
        
        
    def __eval_gross_profit_margin(self, statements:list):
        # a company with a history of gross profit margins abvoe 40% is an early indication that the company has a DCA
        average_margin = self.__calculate_average(statements, 'grossProfit', 'revenue')
        if average_margin >= 40.00:
            print(f'{self.excellent} Gross Profit Margin is above 40% for the last five years at {average_margin}%') 
            self.__points += 1
        elif average_margin >= 30.00: 
            print(f'{self.good} Gross Profit Margin is above 30% for the last five years at {average_margin}%')
            self.__points += 0.5
        else: print(f'{self.poor} Gross Profit Margin is below 30% for the last five years at {average_margin}%')

    def __eval_SGA_expenses(self, statements):
        # a company with SGA expenses as a percentage of gross profits consistently lower than 35% may have a DCA
        # assumed 50% as a middle ground
        average_SGA_expense = self.__calculate_average(statements, 'generalAndAdministrativeExpenses')
        self.__print_summary('Sales and general admin expenses', 35, 50, average_SGA_expense)

        # just getting years for all statements here
        self.__years = [statement['date'][:4] for statement in statements]
    
    def __eval_RD_expenses(self, statements):
        # Buffet indicates that companies with little to none R&D expenses tend to have a DCA working in their favour
        # I have chosen a conservative 15% of gross profits as a middle ground for this entry on the income sheet
        average_RD_expense = self.__calculate_average(statements, 'researchAndDevelopmentExpenses')
        if average_RD_expense == 0.00:
            print(f'{self.excellent} No research and development costs over past five years')
            self.__points += 1
        elif average_RD_expense <= 15.00:
            print(f'{self.good} Research and development costs less than 15% of gross profits over past five years at {average_RD_expense}%')
            self.__points += 0.5
        else:
            print(f'{self.poor} Research and development costs greatar than 15% of gross profits over past five years at {average_RD_expense}%')

    def __eval_depreciation_expenses(self, statements):
        # companies that have low depreciation and amoritzation expenses as a percentage of gross profit tend to have a DCA
        # Buffet does not mention a specific threshold so I went with 10% for the top tier and 15% for the middle tier based off companies with known DCA
        average_depreciation_expense = self.__calculate_average(statements, 'depreciationAndAmortization')
        self.__print_summary('Depreciation and ammortization expenses', 10, 15, average_depreciation_expense)

    def __eval_interest_expense(self, statements):
        # Buffet indicates that companies with interest expenses less than 15% of operating income tend to have a DCA, the lower the better
        # assumed 25% as the middle ground
        average_interest_expense = self.__calculate_average(statements, 'interestExpense', 'operatingIncome')
        self.__print_summary('Interest expenses', 15, 25, average_interest_expense)
        # print(self.__points)

    def __eval_net_income(self, statements):
        # Companies with net income greatar than 20% of total revenues tend to have a DCA
        # Companies with net income less than 10% of total revenues tend to be in an industry with lots of competetion
        # where a single company cannot have an advantage over the others
        average_net_income = self.__calculate_average(statements, 'netIncome', 'revenue')
        if average_net_income >= 20.00:
            print(f'{self.excellent} Net income is at or above 20% of total revenues for the last five years at {average_net_income}%') 
            self.__points += 1
        elif average_net_income >= 10.00: 
            print(f'{self.good} Net income is at or above 10% of total revenues for the last five years at {average_net_income}%')
            self.__points += 0.5
        else: 
            print(f'{self.poor} Net income is below 10% of total revenues for the last five years at {average_net_income}%')

        trend = self.__determine_trend(statements, 'netIncome')
        if trend == 'increasing': 
            self.__points += 1
            print(f'{self.excellent} Net income increasing every year for past five years')
        elif trend == 'decreasing': 
            self.__points -= 1
            print(f'{self.poor} Net income decreasing every year for past five years')

        # populating self.__net_income
        self.__net_income = [statement['netIncome'] for statement in statements]

    def evaluate_balance_sheet(self):
        print(colored(f'-------------------------------EVALUATING BALANCE SHEETS FOR {self.ticker_name}----------------------------------------', 'cyan'))
        statements = self.__get_statement('balance-sheet-statement')
        self.__eval_cash_assets(statements)
        self.__eval_inventory(statements)
        self.__eval_current_ratio(statements)
        self.__eval_goodwill_intangibles(statements)
        self.__eval_return_on_assets(statements)
        self.__eval_long_term_debt(statements)
        self.__eval_retained_earnings(statements)
        # self.__eval_debt_equity_ratio(statements)
        self.__eval_return_shareholder_equity(statements)
        print(' ')

    def __eval_cash_assets(self, statements):
        # Buffet mentions having a large cash pile is good, but does not provide a quantifiable amount
        # He does mention that companies with an up-trend in cash and cash equivalents and low debts are promising signs of a company with a DCA
        trend = self.__determine_trend(statements, 'cashAndCashEquivalents')
        self.__print_trend(trend, 'Cash and cash equivalents')
        
    def __eval_inventory(self, statements):
        # Companies with increasing inventory indicates that there is demand for the product or service and is a sign of a company with a DCA
        # Some companies do not have inventory, if thats the case, no need to evaluate this entry; else, check trend of inventory over five year period
        no_inventory = 0
        for statement in statements:
            if not statement['inventory']: no_inventory += 1
        if no_inventory == len(statements): return

        trend = self.__determine_trend(statements, 'inventory')
        self.__print_trend(trend, 'Inventory')

    def __eval_current_ratio(self, statements):
        # current ratio indicates whether a company can pay off its current liabilities 
        # ratio above 1 indicates company is liquid and can pay off debts; Current Ratio = Current Assets / Current Liabilities
        current_ratio = round(self.__calculate_average(statements, 'totalCurrentAssets', 'totalCurrentLiabilities') / 100, 2)
        if current_ratio >= 1:
            self.__points += 1 
            print(f'{self.excellent} Current ratio is above 1 at {current_ratio}, company is liquid and can pay off its short term debts and obligations')
        else:
            print(f'[NEUTRAL] Current ratio is below 1 at {current_ratio}, consult net earnings to check if company can pay off its short term debts and obligations using earning power')
        
        self.__total_assets = [statement['totalAssets'] for statement in statements]
    
    def __eval_goodwill_intangibles(self, statements):
        # when companies buy other companies at an excess of book value, the excess is stored under goodwill
        # if goodwill is increasing, the company is out buying other companies
        # intangibles are assets such as patents or copyrights that could provide a DCA
        trend = self.__determine_trend(statements, 'goodwillAndIntangibleAssets')
        if trend == 'increasing' or (trend[0] == 'sideways' and trend[1] >= 3):
            print(f'{self.good} Intangibles and goodwill increasing, company is out buying other companies; check which companies, and if those companies also have a DCA')

    def __eval_return_on_assets(self, statements):
        # return on assets is a ratio of how efficiently company management is utilizing assets to generate income; traditionally, the higher the ratio the better
        # however, Buffet indicates that with a high ratio, the company must have low total assets;
        # this would make it easier for someone to raise enough money to compete with said company, making its DCA non-durable
        # whereas companies with good earnings and large total assets have low return on assets 
        # but for that reason its also harder for others to break in to the industry since they have to raise enough total assets to match and compete with the company
        ratio = 0
        total_assets = 0
        for i in range(min(len(statements), len(self.__net_income))):
            assets = statements[i]['totalAssets']
            # checking for divide by zero error
            if not assets: continue
            ratio += self.__net_income[i] / assets * 100
            total_assets += assets
        ratio = round(ratio / len(statements), 2)
        total_assets = round(total_assets / len(statements))
        if ratio < 0:
            print(f'{self.poor} Company has a negative return on assets of {ratio}%')
        elif ratio <= 15:
            print(f'{self.good} Company has a return on assets of {ratio}%, this low ratio may indicate high total assets which provide barrier to entry and enhance DCA; Total Assets: ${total_assets:,}')
        else:
            print(f'{self.good} Company has a return on assets of {ratio}%, this high ratio may indicate low assets which increase ease of entry and diminish DCA; Total Assets: ${total_assets:,}')

    def __eval_long_term_debt(self, statements):
        # Buffet indicates that companies with a DCA have little to none long term debt
        # A good sign is if a company can pay off all its long term debt using its net earnings within 3-4 years, amazing companies can do it under 2
        average_years = 0
        debt_average = 0
        for i in range(min(len(self.__net_income),len(statements))):
           debt = statements[i]['longTermDebt']
           if not self.__net_income[i]: continue
           years_to_pay_off = statements[i]['longTermDebt'] / self.__net_income[i]
           average_years += years_to_pay_off
           debt_average += debt
        average_years /= len(statements)
        debt_average = round(debt_average / len(statements))
        if average_years <= 4:
            self.__points += 1
            print(f'{self.excellent} Long term debt (${debt_average:,}), can be paid off within 4 years using current earnings',)
        elif average_years <= 8:
            self.__points += 0.5
            print(f'{self.good} Long term debt (${debt_average:,}), however, can be paid off within 8 years using current earnings')
        elif average_years > 8:
            print(f'{self.poor} Long term debt (${debt_average:,}), cannot be paid off within 8 years using current earnings')

        self.__long_term_debt = [statement['longTermDebt'] for statement in statements]

    def __eval_return_shareholder_equity(self, statements):
        # higher return the better, one of the best indicators for a company with a DCA
        # some companies have a negative return; if theres a history of strong net earnings, chances are that company also has a DCA
        # chosen thresholds based off companies with known DCA
        average_return = 0
        for i in range(min(len(self.__net_income), len(statements))):
            if statements[i]['totalStockholdersEquity'] == 0: continue
            average_return += self.__net_income[i] / statements[i]['totalStockholdersEquity']
        average_return = round(average_return / len(statements), 2)
        average_return = round(average_return / len(statements), 2)

        if average_return >= 0.3:
            print(f"{self.excellent} High return on shareholders' equity: {average_return}")
        elif average_return >= 0.15:
            print(f"{self.good} Good return on shareholders' equity: {average_return}")
        elif average_return >= 0:
            print(f"{self.poor} Low return on shareholders' equity: {average_return}")
        else:
            print(f"[NEUTRAL] Negative shareholders' equity ({average_return}), if net income history is strong than company has a DCA")

    def __eval_retained_earnings(self, statements):
        # one of the most crucial indicators of a company with a DCA
        # if the retained earnings pool is growing, the company is growing its net worth and will theoretically make us rich also
        trend = self.__determine_trend(statements, 'retainedEarnings')
        self.__print_trend(trend, 'Retained earnings')
        
        self.__retained_earnings = [statement['retainedEarnings'] for statement in statements]
    
    def evaluate_cashflow_statement(self):
        print(colored(f'------------------------------EVALUATING CASH FLOW STATEMENTS FOR {self.ticker_name}-----------------------------------', 'cyan'))
        statements = self.__get_statement('cash-flow-statement')
        self.__evaluate_capital_expenditures(statements)
        self.__eval_stock_repurchase(statements)
        self.__eval_earnings_per_share()

    def __evaluate_capital_expenditures(self, statements):
        # Buffet indicates that companies with capital expenditures less than 50% of net income may have a DCA
        average_capital_expenditures = abs(self.__calculate_average(statements, 'capitalExpenditure', 'netIncome'))
        if average_capital_expenditures <= 50:
            self.__points += 1
            print(f'{self.excellent} Low capital expenditures to net income: {average_capital_expenditures}%')
        else:
            self.__points -= 1
            print(f"{self.poor} High capital expenditures to net income: {average_capital_expenditures}%")

    def __eval_stock_repurchase(self, statements):
        # stock repurchase is excellent sign of a company with a DCA
        self.__stock_repurchased = [-statement['commonStockRepurchased'] for statement in statements]
        years_repurchased = 0
        for statement in statements:
            if statement['commonStockRepurchased']: years_repurchased += 1
        if years_repurchased == len(statements):
            self.__points += 1
            print(f'{self.excellent} Company repurchasing shares each year')
        elif years_repurchased > 0:
            self.__points += 0.5
            print(f'{self.good} Company repruchased shares {years_repurchased}/5 years')
        else:
            self.__points -= 1 
            print(f'{self.poor} Company not repurchasing shares over past 5 years')
        
    def __eval_earnings_per_share(self):
        statements = self.__get_statement('key-metrics')
        trend = self.__determine_trend(statements, "netIncomePerShare")
        self.__print_trend(trend, 'Earnings per share')
        
        # filling in data needed to plot graphs
        self.__earnings_per_share = [statement['netIncomePerShare'] for statement in statements]
        self.__pe_ratio = [statement['peRatio'] for statement in statements]
        self.__market_cap = [statement['marketCap'] for statement in statements]
        self.__dividend_yield = [statement['dividendYield'] for statement in statements]
        self.__current_ratio = [statement['currentRatio'] for statement in statements]

    def get_analysis(self):
        if self.__points >= 8:
            print(f'{self.analysis} Our calculations strongly indicate that this security may posess a DCA and is a good buy for the long term investor')
        elif self.__points >= 6.5:
            print(f'{self.analysis} Our calculations indicate that this security is quite promising and has great potential but does not have a DCA yet')
        else:
            print(f'{self.analysis} Our calculations indicate this security does not posses a valid DCA and is not a good buy for the long term investor')

    def __print_summary(self, entry:str, upper_threshold:int, lower_threshold:int, entry_average:float):
        if entry_average <= upper_threshold:
            print(f'{self.excellent} {entry} less than or equal to {upper_threshold}% of gross profits over past five years at {entry_average}%')
            self.__points += 1
        elif entry_average <= lower_threshold:
            print(f'{self.good} {entry} less than or equal to {lower_threshold}% of gross profits over past five years at {entry_average}%')
            self.__points += 0.5
        else:
            print(f'{self.poor} {entry} greater than {lower_threshold}% of gross profits over past five years at {entry_average}%')
    
    def __print_trend(self, trend:str, entry:str):
        if trend == 'increasing':
            self.__points += 1
            print(f'{self.excellent} {entry} increasing every year for past five years')
        elif trend == 'decreasing': 
            self.__points -= 1
            print(f'{self.poor} {entry} declining every year for past five years')
        elif trend[0] == 'sideways': 
            if trend[1] >= 3: 
                self.__points += 0.5
                print(f'{self.good} {entry} increasing for majority of past five years')
            elif trend[1] <= -3:
                self.__points -= 0.5
                print(f'[OKAY] {entry} decreasing for majority of past five years')
            else:
                print(f'[NEUTRAL] {entry} have no major trend, stable')

    @property
    def plot_values(self):
        values = {
            'years': self.__years,
            'netIncome': self.__net_income,
            'totalAssets': self.__total_assets, 
            'longTermDebt': self.__long_term_debt,
            'retainedEarnings': self.__retained_earnings,
            'EPS': self.__earnings_per_share, 
            'PE': self.__pe_ratio,
            'marketCap': self.__market_cap,
            'dividendYield': self.__dividend_yield,
            'currentRatio': self.__current_ratio,
            'stockRepurchased': self.__stock_repurchased
        }
        return values
