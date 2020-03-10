from datetime import time

import Strategy
from Stock import Stock


class Transaction:

    """
    Stores transaction informations about a trade
    """

    strategy = None
    stock = None
    invested = 0
    date = None
    action = None

    def __init__(self, strategy: Strategy, stock: Stock, invested: int, date: str, action: Strategy.StockActions) -> None:
        super().__init__()

        self.strategy = strategy
        self.stock = stock
        self.invested = invested
        self.date = date
        self.action = action

