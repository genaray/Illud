from datetime import time

import Strategy


class Transaction:

    """
    Stores transaction informations about a trade
    """

    strategy = None
    amount = 0
    date = None
    action = None

    def __init__(self, strategy: Strategy, amount: int, date: str, action: Strategy.StockActions) -> None:
        super().__init__()

        self.strategy = strategy
        self.amount = amount
        self.date = date
        self.action = action

