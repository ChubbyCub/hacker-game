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
        if display == COLLECTABLE:
            return Collectable('C')
        if display == BLOCKER:
            return Blocker('B')
        if display == DESTROYABLE:
            return Destroyable('D')
        if display == PLAYER:
            return Player('P')
        else:
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
        curr_entities_map = self.grid.get_entities()

        if direction == DIRECTIONS[0]:
            offset = Position(ROTATIONS[0][0], ROTATIONS[0][1])
            self._helper(direction, offset, curr_entities_map)
        elif direction == DIRECTIONS[1]:
            offset = Position(ROTATIONS[1][0], ROTATIONS[1][1])
            self._helper(direction, offset, curr_entities_map)
        else:
            raise NotImplementedError

    def _helper(
        self,
        direction: str,
        offset: Position,
        curr_entities_map: dict[Position, Entity]
    ) -> None:
        for position, entity in curr_entities_map.items():
            new_position = position.add(offset)
            """
                the only time that it is not inbounds for left rotation is when the
                entity is at column 0 and we shift it to the left once more.
                the only time that it is not inbounds for right rotation is when the
                entity is at column size - 1 and we shift it to the right once more.
                case in point: check if is in bounds, if it is not then we will fix the column accordingly
            """
            if not self.grid.in_bounds(new_position):
                x = new_position.get_x()
                y = self.grid.get_size() - 1 if direction == DIRECTIONS[0] else 0
                new_position = Position(x, y)
            # it is ok to overwrite the key in the existing map because the new_position object is a different
            # position; hence, will have different hash value and will make a new entry in the map
            curr_entities_map[new_position] = entity

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
