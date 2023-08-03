from goodwe_connector.strategy import Strategy
from goodwe_connector.goodwe_api import GoodweApi
class GoodweContext():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, goodwe_api:GoodweApi, strategy: Strategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """
        self.__goodwe_api = goodwe_api
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def process(self) -> object:

        result = self._strategy.do_algorithm(self.__goodwe_api)
    
        return result