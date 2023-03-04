from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime

class Creator(ABC):

    @abstractmethod
    def factory_method(self):

        pass

    def some_operation(self) -> str:

        # Call the factory method to create a Product object.
        product = self.factory_method()

        # Now, use the product.
        result = f"Creator: The same creator's code has just worked with {product.operation()}"

        return result

# Product
class GoodweMetric(ABC):

    @abstractmethod
    def operation(self) -> dict:
        pass

class PowerGenerationInDay(Creator):
    
    def __init__(self, date_argument:datetime) -> None:
        
        self.date = date_argument
        
        super().__init__()
    
    def factory_method(self) -> GoodweMetric:
        return PowerGenerationInDayMetric(self.date)

class PowerGenerationInDayBetweenDates(Creator):
    def __init__(self, start_date_arg:datetime, end_date_arg:datetime) -> None:
        
        self.start_date = start_date_arg
        self.end_date = end_date_arg
        
        super().__init__()
    
    def factory_method(self) -> GoodweMetric:
        return PowerGenerationInDayBetweenDatesMetric(self.start_date, self.end_date)


class PowerGeneratedInADayEveryFiveMinutes(Creator):
    
    def __init__(self, date_argument:datetime) -> None:
        
        self.date = date_argument
        
        super().__init__()
    
    def factory_method(self) -> GoodweMetric:
        return PowerGeneratedInADayEveryFiveMinutesMetric(self.date)

class PowerGenerationInDayMetric(GoodweMetric):
    def __init__(self, date:datetime) -> None:
    
        self.date = date
    
    def operation(self) -> str:
        # TODO:
        # def get_power_generation_per_day(self, date:datetime) -> float:
        return f'[Result of the PowerGenerationInDayMetric] date: {self.date}'


class PowerGenerationInDayBetweenDatesMetric(GoodweMetric):
    
    def __init__(self, start_date_arg:datetime, end_date_arg:datetime) -> None:
        
        self.start_date = start_date_arg
        self.end_date = end_date_arg
    
    def operation(self) -> str:
        # TODO:
        # def get_power_generation_between_dates(self, start_date:datetime, end_date:datetime) -> dict:
        return f'[Result of the PowerGenerationInDayBetweenDatesMetric] start_date: {self.start_date}, end_date: {self.end_date}'


class PowerGeneratedInADayEveryFiveMinutesMetric(GoodweMetric):

    def __init__(self, date:datetime) -> None:
    
        self.date = date
    
    def operation(self) -> str:
        # TODO:
        # def get_power_station_generated_every_five_minutes_per_day(self, date:datetime) -> dict:
        return f'[Result of the PowerGeneratedInADayEveryFiveMinutesMetric] date: {self.date}'
    
    
def client_code(creator: Creator) -> None:
    
    print(f"Client: I'm not aware of the creator's class, but it still works.\n"
          f"{creator.some_operation()}", end="")


if __name__ == "__main__":
    print(f'App: Launched with the PowerGenerationInDay')
    client_code(PowerGenerationInDay(date_argument=datetime(2023,4,5)))
    print("\n")
    
    print(f'App: Launched with the PowerGenerationInDayBetweenDates.')
    client_code(PowerGenerationInDayBetweenDates(start_date_arg=datetime(2023,4,5), end_date_arg=datetime(2023,5,5)))
    print("\n")

    print(f'App: Launched with the PowerGeneratedInADayEveryFiveMinutes.')
    client_code(PowerGeneratedInADayEveryFiveMinutes(date_argument=datetime(2025,4,2)))
    print("\n")
    
