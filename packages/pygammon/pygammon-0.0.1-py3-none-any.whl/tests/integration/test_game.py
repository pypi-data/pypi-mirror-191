import unittest
from copy import deepcopy
from pathlib import Path
from typing import Set, Tuple, cast

from pygammon.core import Game
from pygammon.exceptions import MaxMovesFound
from pygammon.structures import Point, Side


def read_game(fixture_index: int) -> Game:
    def read_pair(line_number: int) -> Tuple[int, int]:
        map_object = map(int, contents[line_number].split())
        return cast(Tuple[int, int], tuple(map_object))

    game = Game(Side.FIRST)
    fixture_path = Path(__file__).parent / f"fixtures/{fixture_index}"
    contents = fixture_path.read_text().splitlines()
    first_row = contents[0].split()
    second_row = reversed(contents[1].split())

    for i, cell in enumerate([*second_row, *first_row]):
        if cell == "0":
            game.board[i] = Point()
        else:
            side = Side.FIRST if cell[-1] == "f" else Side.SECOND
            count = int(cell[:-1])
            game.board[i] = Point(side, count)

    first_player = game.players[Side.FIRST]
    second_player = game.players[Side.SECOND]
    first_player.hit, first_player.borne = read_pair(2)
    second_player.hit, second_player.borne = read_pair(3)

    game.dice = read_pair(4)
    if game.dice[0] == game.dice[1]:
        game.dice *= 2

    game.side = Side.FIRST if contents[5] == "1" else Side.SECOND

    return game


GAME_EXAMPLES = [read_game(i) for i in range(3)]


def game_example(index: int) -> Game:
    return deepcopy(GAME_EXAMPLES[index])


class TestAddMoveCount(unittest.TestCase):
    def test_max_moves_found(self) -> None:
        for fixture_index, source in [(0, 12), (2, 6)]:
            game = game_example(fixture_index)
            with self.assertRaises(MaxMovesFound):
                game._add_move_count(0, source, set())

    def test_invalid_move(self) -> None:
        game = game_example(0)
        move_counts: Set[int] = set()
        game._add_move_count(3, 5, move_counts)
        self.assertEqual(move_counts, set())

    def test_limited(self) -> None:
        game = game_example(1)
        move_counts = {0}
        game._add_move_count(0, 1, move_counts)
        self.assertEqual(move_counts, {0, 1})


class TestGetMoveCount(unittest.TestCase):
    def test_max_moves_found(self) -> None:
        for fixture_index in [0, 2]:
            game = game_example(fixture_index)
            with self.assertRaises(MaxMovesFound):
                game._get_move_count()

    def test_limited(self) -> None:
        game = game_example(1)
        move_count = game._get_move_count()
        self.assertEqual(move_count, 1)


class TestGetMaxMoveCount(unittest.TestCase):
    def test_max_moves_found(self) -> None:
        game_a = Game(Side.FIRST)
        game_a.dice = 3, 3, 3, 3
        max_move_count_a = game_a.get_max_move_count()
        self.assertEqual(max_move_count_a, 4)

        game_b = game_example(0)
        max_move_count_b = game_b.get_max_move_count()
        self.assertEqual(max_move_count_b, 2)
