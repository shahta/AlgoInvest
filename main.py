import argparse
from src.TickerEval import TickerEval
from src.BalanceSheet import BalanceSheet
from src.IncomeStatement import IncomeStatement
import time



parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker')
args = parser.parse_args()


ticker = args.ticker

symbol = TickerEval(ticker)
# symbol_income = IncomeStatement(ticker)
# symbol_balance = BalanceSheet(ticker)
symbol.evaluate_income_statement()
symbol.evaluate_balance_sheet()

