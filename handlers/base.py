from abc import ABC, abstractmethod

# Abstract base class for all query handlers (Strategy pattern)
class QueryHandler(ABC):
    @abstractmethod
    def run(self, query: str) -> str:
        pass 