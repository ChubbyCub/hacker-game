from src.a3_support import Position
from src.models.Entity import Entity


class Grid:
    def __init__(self, size: int) -> None:
        self.size = size
        self.container = {}

    def get_size(self) -> int:
        return self.size

    def add_entity(self, position: Position, entity: Entity) -> None:
        if not self.in_bounds(position):
            raise IndexError
        self.container[position] = entity

    def get_entities(self) -> dict[Position, Entity]:
        return self.container

    def get_entity(self, position: Position) -> Entity or None:
        return self.container[position]

    def remove_entity(self, position: Position) -> Position or None:
        self.container.pop(position, None)

    def serialise(self) -> dict[tuple[int, int], str]:
        serialized_grid = {}
        for key, value in self.container.items():
            if key not in serialized_grid:
                serialized_grid[(key.get_x(), key.get_y())] = value.display()
        return serialized_grid

    def in_bounds(self, position: Position) -> bool:
        x = position.get_x()
        y = position.get_y()
        return 0 <= x < self.size and 1 <= y < self.size

    def __repr__(self) -> str:
        return f"Grid({self.size})"
