from abc import ABC

from src.models.Entity import Entity


class Collectable(Entity, ABC):
    def __init__(self, name):
        super().__init__(name)

    def display(self) -> str:
        return self.name
