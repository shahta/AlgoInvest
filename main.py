import argparse
from src.TickerEval import TickerEval

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker')
args = parser.parse_args()

ticker = args.ticker
symbol = TickerEval(ticker)
print(f'Evaluating income statements for {ticker}')
symbol.evaluate_income_statement()
