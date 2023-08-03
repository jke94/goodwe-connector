from abc import ABC, abstractmethod
from goodwe_connector.goodwe_api import GoodweApi
# from goodwe_connector.goodwe_api import GoodweApi
from typing import List

class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def do_algorithm(self, goodwe:GoodweApi):
        pass