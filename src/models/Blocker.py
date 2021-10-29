from src.models.Entity import Entity


class Blocker(Entity):
    def __init__(self, name):
        super().__init__(name)

    def display(self) -> str:
        return self.name
