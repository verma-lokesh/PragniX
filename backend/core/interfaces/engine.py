from abc import ABC, abstractmethod


class Engine(ABC):
    name: str = "engine"

    @abstractmethod
    def execute(self, context) -> None:
        """Mutate the shared ExecutionContext with this engine's results."""
        raise NotImplementedError
