from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def display(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
