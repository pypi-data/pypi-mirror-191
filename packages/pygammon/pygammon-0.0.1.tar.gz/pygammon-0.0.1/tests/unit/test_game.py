import unittest
from contextlib import contextmanager
from typing import Iterator, Optional, Set, Tuple, Union, cast
from unittest.mock import Mock, patch

from pygammon.core import Game
from pygammon.exceptions import GameWon, InvalidMove, MaxMovesFound
from pygammon.structures import (
    BOARD_SIZE,
    DIE_FACE_COUNT,
    SIDE_PIECE_COUNT,
    GameState,
    InvalidMoveCode,
    OutputType,
    Point,
    Side,
)

MOVE_COUNT_EXAMPLES = [2, 3]


class GameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(Side.FIRST)
        self.player = self.game.players[self.game.side]


class TestRollDice(GameTestCase):
    @patch("pygammon.core.randint")
    def test_calls(self, mock_randint: Mock) -> None:
        self.game.roll_dice()

        mock_randint.assert_called_with(1, DIE_FACE_COUNT)
        self.assertEqual(mock_randint.call_count, 2)

    def test_basics(self) -> None:
        self.game.roll_dice()

        self.assertIn(len(self.game.dice), {2, 4})

        for die in self.game.dice:
            self.assertGreaterEqual(die, 1)
            self.assertLessEqual(die, DIE_FACE_COUNT)

    @patch("pygammon.core.randint", return_value=3)
    def test_count(self, mock_randint: Mock) -> None:
        self.game.roll_dice()
        self.assertEqual(len(self.game.dice), 4)

        mock_randint.side_effect = 4, 5
        self.game.roll_dice()
        self.assertEqual(len(self.game.dice), 2)


class TestMove(GameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.game.dice = 3, 4

    def check_invalid_move(
        self,
        die_index: int,
        source: Optional[int],
        code: InvalidMoveCode,
        data: Optional[int],
    ) -> None:
        with self.assertRaises(InvalidMove) as context_manager:
            self.game.move(die_index, source)

        self.assertEqual(context_manager.exception.code, code)
        self.assertEqual(context_manager.exception.data, data)

    def check_invalid_die_index(
        self, die_index: int, source: Optional[int], code: InvalidMoveCode
    ) -> None:
        self.check_invalid_move(die_index, source, code, die_index)

    def check_invalid_source(
        self, die_index: int, source: Optional[int], code: InvalidMoveCode
    ) -> None:
        self.check_invalid_move(die_index, source, code, source)

    def test_die_already_played(self) -> None:
        ALREADY_PLAYED_INDEX = 1
        SOURCE = 5
        self.game.dice_played = {ALREADY_PLAYED_INDEX}

        self.check_invalid_die_index(
            ALREADY_PLAYED_INDEX, SOURCE, InvalidMoveCode.DIE_INDEX_INVALID
        )

    def test_die_nonexistent(self) -> None:
        NONEXISTENT_INDEX = len(self.game.dice)

        self.check_invalid_die_index(
            NONEXISTENT_INDEX, 7, InvalidMoveCode.DIE_INDEX_INVALID
        )

    def test_hit_source_not_none(self) -> None:
        SOURCE = 12
        self.player.hit = 3

        self.check_invalid_source(0, SOURCE, InvalidMoveCode.SOURCE_INVALID)

    def test_not_hit_source_none(self) -> None:
        self.check_invalid_source(1, None, InvalidMoveCode.SOURCE_INVALID)

    def test_not_hit_source_nonexistent(self) -> None:
        DIE_INDEX = 0
        NONEXISTENT_SOURCE = len(self.game.board)

        self.check_invalid_source(
            DIE_INDEX, NONEXISTENT_SOURCE, InvalidMoveCode.SOURCE_INVALID
        )

    def test_not_hit_source_not_owned(self) -> None:
        DIE_INDEX = 0
        NOT_OWNED_SOURCE = 0

        self.check_invalid_source(
            DIE_INDEX, NOT_OWNED_SOURCE, InvalidMoveCode.SOURCE_NOT_OWNED_PIECE
        )

    def get_destination(self, die_index: int, source: int) -> int:
        return source + self.game.dice[die_index] * self.player.direction

    def check_invalid_destination(
        self, dice: Tuple[int, int], die_index: int, source: int, code: InvalidMoveCode
    ) -> None:
        self.game.dice = dice

        destination = self.get_destination(die_index, source)
        self.check_invalid_move(die_index, source, code, destination)

    def test_destination_occupied(self) -> None:
        DICE = 4, 5
        DIE_INDEX = 1
        SOURCE = BOARD_SIZE - 1

        self.check_invalid_destination(
            DICE, DIE_INDEX, SOURCE, InvalidMoveCode.DESTINATION_OCCUPIED
        )

    def test_destination_out_of_board(self) -> None:
        DICE = 6, 2
        DIE_INDEX = 0
        SOURCE = 5

        self.check_invalid_destination(
            DICE, DIE_INDEX, SOURCE, InvalidMoveCode.DESTINATION_OUT_OF_BOARD
        )

    @contextmanager
    def check_play_new_die(self, die_index: int) -> Iterator[None]:
        try:
            self.assertNotIn(die_index, self.game.dice_played)
            yield
        finally:
            self.assertIn(die_index, self.game.dice_played)

    def test_hit(self) -> None:
        DIE_INDEX = 0
        HIT = 1
        self.player.hit = HIT

        with self.check_play_new_die(DIE_INDEX):
            self.game.move(DIE_INDEX, None)

        destination_point = self.game.board[BOARD_SIZE - self.game.dice[DIE_INDEX]]
        self.assertEqual(destination_point, Point(self.game.side, 1))
        self.assertEqual(self.player.hit, HIT - 1)

    def test_move(self) -> None:
        DIE_INDEX = 0
        SOURCE = 7

        with self.check_play_new_die(DIE_INDEX):
            self.game.move(DIE_INDEX, SOURCE)

        destination = self.get_destination(DIE_INDEX, SOURCE)
        self.assertEqual(self.game.board[destination], Point(self.game.side, 1))

    def test_hit_opponent(self) -> None:
        DIE_INDEX = 0
        SOURCE = 5
        destination = self.get_destination(DIE_INDEX, SOURCE)
        opponent_side = Side(not self.game.side)
        self.game.board[destination] = Point(opponent_side, 1)

        with self.check_play_new_die(DIE_INDEX):
            self.game.move(DIE_INDEX, SOURCE)

        self.assertEqual(self.game.board[destination], Point(self.game.side, 1))
        self.assertEqual(self.game.players[opponent_side].hit, 1)

    def test_bearing_off(self) -> None:
        self.game.dice = 6, 2
        DIE_INDEX = 0
        SOURCE = 5
        previously_borne = self.player.borne

        for point_index in [7, 12, 23]:
            self.game.board[point_index] = Point()

        self.game.move(DIE_INDEX, SOURCE)
        self.assertEqual(self.player.borne, previously_borne + 1)

    def test_last_piece_on_point(self) -> None:
        DIE_INDEX = 0
        SOURCE = 12
        point = self.game.board[SOURCE]
        point.count = 1

        self.assertEqual(point.side, self.game.side)
        self.game.move(DIE_INDEX, SOURCE)
        self.assertIsNone(point.side)

    def test_game_won(self) -> None:
        self.player.borne = SIDE_PIECE_COUNT
        with self.assertRaises(GameWon):
            self.game.move(0, 5)


@patch("pygammon.core.Game.move")
@patch("pygammon.core.Game._get_move_count", return_value=MOVE_COUNT_EXAMPLES[0])
class TestAddMoveCount(GameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.move_counts: Set[int] = set()

    def test_calls(self, mock_get_move_count: Mock, mock_move: Mock) -> None:
        DIE_INDEX = 0
        SOURCE = 7
        self.game._add_move_count(DIE_INDEX, SOURCE, set())

        mock_move.assert_called_once_with(DIE_INDEX, SOURCE)
        mock_get_move_count.assert_called_once_with()

    def test_valid_move(self, _mock_get_move_count: Mock, _mock_move: Mock) -> None:
        DIE_INDEX = 0
        SOURCE = 7
        self.game._add_move_count(DIE_INDEX, SOURCE, self.move_counts)
        self.assertEqual(self.move_counts, {1 + MOVE_COUNT_EXAMPLES[0]})

    def test_invalid_move(self, _mock_get_move_count: Mock, mock_move: Mock) -> None:
        DIE_INDEX = 1
        SOURCE = -3
        mock_move.side_effect = InvalidMove(InvalidMoveCode.SOURCE_INVALID, SOURCE)
        self.game._add_move_count(DIE_INDEX, SOURCE, self.move_counts)
        self.assertEqual(self.move_counts, set())


@patch("pygammon.core.Game._add_move_count")
class TestGetMoveCount(GameTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.game.dice = 5, 3
        self.die_count = len(self.game.dice)

    def test_max_moves_found(self, mock_add_move_count: Mock) -> None:
        self.game.dice_played = {0, 1}

        with self.assertRaises(MaxMovesFound):
            self.game._get_move_count()

        mock_add_move_count.assert_not_called()

    def test_zero_moves_added(self, mock_add_move_count: Mock) -> None:
        move_count = self.game._get_move_count()

        self.assertEqual(move_count, 0)
        mock_add_move_count.assert_called()

    def check_nonzero_moves_added(
        self, hit: int, calls_per_die: int, mock_add_move_count: Mock
    ) -> None:
        MOVE_COUNT = 4

        def add_sample_count(
            die_index: int, _source: Optional[int], move_counts: Set[int]
        ) -> None:
            move_counts.add(MOVE_COUNT - die_index % 2)

        mock_add_move_count.side_effect = add_sample_count
        self.player.hit = hit

        move_count = self.game._get_move_count()
        self.assertEqual(move_count, MOVE_COUNT)
        self.assertEqual(mock_add_move_count.call_count, self.die_count * calls_per_die)

    def test_nonzero_moves_added_hit(self, mock_add_move_count: Mock) -> None:
        self.check_nonzero_moves_added(2, 1, mock_add_move_count)

        for die_index in range(self.die_count):
            (
                die_index_arg,
                source_arg,
                move_counts_arg,
            ) = mock_add_move_count.call_args_list[die_index].args

            self.assertEqual(die_index_arg, die_index)
            self.assertIsNone(source_arg)
            self.assertIsInstance(move_counts_arg, set)

    def test_nonzero_moves_added_not_hit(self, mock_add_move_count: Mock) -> None:
        self.check_nonzero_moves_added(0, BOARD_SIZE, mock_add_move_count)

        for die_index in range(self.die_count):
            for source in range(BOARD_SIZE):
                call_index = die_index * BOARD_SIZE + source
                (
                    die_index_arg,
                    source_arg,
                    move_counts_arg,
                ) = mock_add_move_count.call_args_list[call_index].args

                self.assertEqual(die_index_arg, die_index)
                self.assertEqual(source_arg, source)
                self.assertIsInstance(move_counts_arg, set)


@patch("pygammon.core.Game._get_move_count", return_value=MOVE_COUNT_EXAMPLES[1])
class TestMaxGetMoveCount(GameTestCase):
    def test_no_exception(self, mock_get_move_count: Mock) -> None:
        max_move_count = self.game.get_max_move_count()
        self.assertEqual(max_move_count, MOVE_COUNT_EXAMPLES[1])
        mock_get_move_count.assert_called_once_with()

    def test_exception(self, mock_get_move_count: Mock) -> None:
        mock_get_move_count.side_effect = MaxMovesFound

        for dice, expected_count in ((1, 4), 2), ((3, 3, 3, 3), 4):
            self.game.dice = cast(
                Union[Tuple[int, int], Tuple[int, int, int, int]], dice
            )
            max_move_count = self.game.get_max_move_count()

            self.assertEqual(max_move_count, expected_count)
            mock_get_move_count.assert_called_once_with()
            mock_get_move_count.reset_mock()


class TestSendState(GameTestCase):
    def test_calls(self) -> None:
        FIRST_HIT = 2
        FIRST_BORNE = 0
        SECOND_HIT = 1
        SECOND_BORNE = 6
        first_player = self.game.players[Side.FIRST]
        second_player = self.game.players[Side.SECOND]

        first_player.hit = FIRST_HIT
        first_player.borne = FIRST_BORNE
        second_player.hit = SECOND_HIT
        second_player.borne = SECOND_BORNE

        send_output_mock = Mock()
        self.game.send_state(send_output_mock)

        game_state = GameState(
            self.game.board, FIRST_HIT, FIRST_BORNE, SECOND_HIT, SECOND_BORNE
        )
        send_output_mock.assert_called_once_with(OutputType.GAME_STATE, game_state)
