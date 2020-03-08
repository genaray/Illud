import json

class Stock:

    """
    Represents a stock curled from the web api
    """

    date = "";
    open = 0;
    high = 0;
    low = 0;
    close = 0;
    volume = 0;

    def __init__(self, date: str, open: int, high: int, low: int, close: int, volume: int) -> None:
        super().__init__()

        self.date = date;
        self.open = open;
        self.high = high;
        self.low = low;
        self.close = close;
        self.volume = volume;

    def toJSON(self) -> str:

        """
        :return: The stock in json string format
        :rtype: str
        Converts the stock to its json and returns it as a string.
        """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



