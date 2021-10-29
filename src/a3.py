from a3_support import *
import tkinter as tk
import random

from src.models import Entity
from src.models.Blocker import Blocker
from src.models.Collectable import Collectable
from src.models.Destroyable import Destroyable
from src.models.Grid import Grid
from src.models.Player import Player


class Game:
    def __init__(self, size: int) -> None:
        self.is_won = False
        self.grid = Grid(size)
        self.total_shots = 0

        player = self._create_entity('P')
        self.player_position = Position(0, int(self.grid.size / 2))
        self.grid.add_entity(self.player_position, player)

    def get_grid(self) -> Grid:
        return self.grid

    def get_player_position(self) -> Position:
        return self.player_position

    def get_num_collected(self) -> int:
        num_collectables = 0
        for value in self.grid.container.values():
            if value.display() == 'C':
                num_collectables += 1
        return num_collectables

    def get_num_destroyed(self) -> int:
        num_destroys = 0
        for value in self.grid.container.values():
            if value.display() == 'D':
                num_destroys += 1
        return num_destroys

    def _create_entity(self, display: str) -> Entity:
        match display:
            case 'C':
                return Collectable('C')
            case 'B':
                return Blocker('B')
            case 'D':
                return Destroyable('D')
            case 'P':
                return Player('P')
            case _:
                raise NotImplementedError

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # bomb = False
        # if not blocker:
        #     bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # if bomb:
        #     total_count += 1
        #     entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def get_total_shots(self) -> int:
        return self.total_shots

    def rotate_grid(self, direction: str) -> None:
        grid = self.grid
        entities_map = grid.container

        match direction:
            case 'LEFT':
                offset = Position(-1, 0)
                for position, entity in entities_map.items():
                    new_position = position.add(offset)
                    if grid.in_bounds(new_position):
                        entities_map[new_position] = entity
                    else:
                        rotated_position = Position(new_position.get_x(), self.grid.size - 1)
                        entities_map[rotated_position] = entity
            case 'RIGHT':
                offset = Position(1, 0)
                for position, entity in entities_map.items():
                    new_position = position.add(offset)
                    if grid.in_bounds(new_position):
                        entities_map[new_position] = entity
                    else:
                        rotated_position = Position(new_position.get_x(), 0)
                        entities_map[rotated_position] = entity
            case _:
                raise NotImplementedError

    def step(self) -> None:
        pass

    def fire(self, shot_type: str):
        pass

    def has_won(self) -> bool:
        return self.is_won

    def has_lost(self) -> bool:
        return not self.is_won


def start_game(root, TASK=TASK):
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app


def main():
    root = tk.Tk()
    root.title(TITLE)
    app = start_game(root)
    root.mainloop()


if __name__ == '__main__':
    main()
