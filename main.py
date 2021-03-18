from src.TickerEval import TickerEval

ticker = 'KO'
coke = TickerEval(ticker)
print(f'Evaluating income statements for {ticker}')
coke.evaluate_income_statement()
