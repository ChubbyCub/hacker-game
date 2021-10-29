class Entity:
    def __init__(self, name):
        self.name = name

    def display(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
