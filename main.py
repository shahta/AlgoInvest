import argparse
from src.TickerEval import TickerEval
from src.TrendPlot import TrendPlot
import time


# start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker')
args = parser.parse_args()


ticker = args.ticker


symbol = TickerEval(ticker.upper())
symbol.evaluate_income_statement()
symbol.evaluate_balance_sheet()
symbol.evaluate_cashflow_statement()

trend_graph = TrendPlot(symbol.plot_values)
trend_graph.plot()
# print(round(time.time() - start, 2))