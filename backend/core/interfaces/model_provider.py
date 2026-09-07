from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def predict(self, features: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError
