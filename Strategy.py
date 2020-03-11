import enum
import clone

from Stock import Stock

class StockActions(enum.Enum):
    """
    Possible stock actions...
    """
    LONG=1
    SHORT=2
    STAY=3

class Strategy:

    __currentStock = None           # Our current stock
    __action = None                 # Our current choosen action
    __shareAmount = 10              # Our current calculated share amount

    __lastBoughtStock = None        # Our last bought stock
    __lastAction = None             # Our last choosen action
    __lastTradeAction = None        # Our last action which occured in a trade change ( Long/Short, without Stay )
    __lastShareAmount = 10          # Our last calculated share amount

    """
    A default strategy which runs every stock update to determine if we should hold
    or sell a position...
    """

    def single(self):

        """
        :return: The mode in which this strategy runs...
        :rtype: bool
        """

        return True

    def process(self, stock: Stock):

        """
        :param stock: The stock we analyze
        :type stock: Stock
        :return: Nothing
        :rtype: void
        Gets called by looping over all recorded stocks for processing the strategy.
        """

        # Buy first stock
        if self.__lastBoughtStock is None:
            self.__lastAction = self.__action
            self.__action = StockActions.LONG

        # Otherwhise buy a new stock if its worth more... or sell it promptly.
        if self.__lastBoughtStock is not None:

            if stock.high > self.__lastBoughtStock.high:
                self.__lastAction = self.__action
                self.__action = StockActions.LONG
            elif stock.high < self.__lastBoughtStock.high:
                self.__lastAction = self.__action
                self.__action = StockActions.SHORT
            else:
                self.__lastAction = self.__action
                self.__action = StockActions.STAY

        self.__lastBoughtStock = self.__currentStock
        self.__currentStock = stock
        pass


    def action(self):

        """
        :return: True if this strategy decided that we should buy the stock for long
        :rtype: StockActions
        Lets the strategy determine if we should buy the stock for long ( profit whise ) or short...
        """

        # Remembering our last "real" trade action... not staying
        if self.__lastAction is not StockActions.STAY:
            self.__lastTradeAction = self.__lastAction

        return self.__action


    def invest(self):

        """
        :return: The amount of shares this strategy decided to buy
        :rtype: int
        Returns the share amount in $ this strategy decided to invest in.
        """

        # Increase investment when we made a loss with out last bough stock
        if self.__lastTradeAction is StockActions.SHORT and self.__action is StockActions.LONG:

            difference = float(self.__lastBoughtStock.high)-float(self.__currentStock.high)
            difference = difference if self.__lastTradeAction is StockActions.LONG else -1*difference

            # Invest double the amount if we made a loss
            if difference < 0:
                self.__shareAmount = self.__lastShareAmount * 2

        self.__lastShareAmount = self.__shareAmount
        return self.__shareAmount