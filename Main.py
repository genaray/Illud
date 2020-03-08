import json
import time
import _collections;
from datetime import datetime

from Stock import Stock
from Curler import Curler
from Strategy import Strategy, StockActions
from Transaction import Transaction

apiAcess = "https://www.alphavantage.co/query?" \
           "function=TIME_SERIES_INTRADAY&" \
           "symbol=AAPL&" \
           "interval=5min&" \
           "outputsize=compact&" \
           "datatype=json&" \
           "apikey=IMA31P07MG9SPXRA";

intervallSEC = (60/5)
stocks = _collections.deque(maxlen=50)

strategys = [Strategy()]
investHistory = {}
wealth = 1000.0;

# Main method starts curler and endless loop.
if __name__ == '__main__':

    curler = Curler()
    singleStrategys = list(filter(lambda x: x.single(), strategys))

    while True:

        # Curling stocks
        jsonWebAPI = curler.curl(apiAcess)
        webAPIResult = json.loads(jsonWebAPI)

        lastRefreshDate = webAPIResult["Meta Data"]["3. Last Refreshed"]
        stockJSON = webAPIResult["Time Series (5min)"][lastRefreshDate]

        print("<--- Midas curling new stock updates from ["+str(lastRefreshDate)+"]--->");

        # Creating stock and appending to ringbuffer
        stock = Stock(
            lastRefreshDate,
            stockJSON["1. open"],
            stockJSON["2. high"],
            stockJSON["3. low"],
            stockJSON["4. close"],
            stockJSON["5. volume"]
        )

        stocks.append(stock)

        # Updating single strategys
        for singleStrategy in singleStrategys:
            singleStrategy.process(stock)

        # Updating strategys needing all recorded stocks
        for strategy in strategys:
            if strategy.single():
                continue
            for stock in stocks:
                strategy.process(stock)

        # Recording transactions
        for strategy in strategys:
            if strategy.action() is not StockActions.STAY:

                lastTransaction = investHistory[strategy][-1] if strategy in investHistory else None
                newTransaction = Transaction(strategy, -strategy.invest(), str(datetime.now()), strategy.action())

                # Prevent same transactions over and over again... you cant to 3 times long in a row
                if lastTransaction is not None and lastTransaction.action is newTransaction.action: continue

                if strategy in investHistory:
                    investHistory[strategy].append(newTransaction)
                else: investHistory[strategy] = [newTransaction]

                wealth += -lastTransaction.amount if lastTransaction is not None else 0
                wealth += newTransaction.amount

        # Checking for what the strategys decided
        for strategy in strategys:
            if strategy.action() is not StockActions.STAY:
                print("<Midas : Strategy [" + type(strategy).__name__ +"] "
                       "decided for [" + str(strategy.action()) + "] "
                       "with a share amount of [" + str(strategy.invest()) + "] "
                       "and a total profit of ["+str(strategy.volume())+"]>")

        # Calculating new wealth using the strategy profit/loss
        for strategy in strategys:
                wealth += strategy.volume()

        print("<Midas : Current wealth "+str(wealth))
        print("<Midas : Last stocks update : "+str(stock.toJSON())+">")
        time.sleep(intervallSEC)


