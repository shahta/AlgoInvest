import argparse
from src.Config import Config
from src.TickerEval import TickerEval
import requests
from termcolor import colored

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker')
args = parser.parse_args()

ticker = args.ticker
ticker_name = ''
stocks = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={Config.KEY}').json()
for stock in stocks:
    if stock['symbol'] == ticker: 
        ticker_name = stock['name'].upper()
        break

symbol = TickerEval(ticker)
print(colored(f'-------------------------------EVALUATING INCOME STATEMENTS FOR {ticker_name}-------------------------------------', 'green'))
symbol.evaluate_income_statement()
print(colored(f'-------------------------------EVALUATING BALANCE SHEETS FOR {ticker_name}-------------------------------------', 'green'))
symbol.evaluate_balance_sheet()