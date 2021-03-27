import argparse
import threading
from src.TickerEval import TickerEval
from src.TrendPlot import TrendPlot
import time


start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker')
args = parser.parse_args()


ticker = args.ticker


symbol = TickerEval(ticker.upper())
t1 = threading.Thread(symbol.evaluate_income_statement())
t2 = threading.Thread(symbol.evaluate_balance_sheet())
t3 = threading.Thread(symbol.evaluate_cashflow_statement())
t1.start()
t1.join()
t2.start()
# t2.join()
t3.start()
# t3.join()
print(time.perf_counter())
trend_graph = TrendPlot(symbol.plot_values, symbol.ticker_name)
t4 = threading.Thread(trend_graph.plot_metrics())
t4.start()
t2.join()
t3.join()
t4.join()




   
    