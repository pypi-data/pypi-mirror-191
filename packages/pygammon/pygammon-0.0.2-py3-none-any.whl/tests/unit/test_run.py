import unittest
from typing import Any, List, Optional, Tuple
from unittest.mock import Mock, patch

from pygammon.core import Game, run
from pygammon.exceptions import GameWon, InvalidMove
from pygammon.structures import (
    DIE_FACE_COUNT,
    DieRolls,
    InputType,
    InvalidMoveCode,
    OutputType,
    Side,
)

DIE_ROLL_HIGH_EXAMPLE = 5
DIE_ROLL_LOW_EXAMPLE = 1
DIE_ROLLS_EXAMPLE = 3, 4


def sample_roll_dice(self: Any) -> None:
    self.dice = DIE_ROLLS_EXAMPLE


@patch(
    "pygammon.core.choice", side_effect=(DIE_ROLL_HIGH_EXAMPLE, DIE_ROLL_LOW_EXAMPLE)
)
@patch("pygammon.core.Game.send_state")
@patch("pygammon.core.Game.roll_dice", autospec=True, side_effect=sample_roll_dice)
@patch("pygammon.core.Game.get_max_move_count", return_value=2)
@patch("pygammon.core.Game.move", side_effect=GameWon)
class TestRun(unittest.TestCase):
    def setUp(self) -> None:
        self.example_move = 0, 5
        self.receive_input = Mock(return_value=(InputType.MOVE, self.example_move))

    def check_calls(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
        expected_send_state_call_count: int = 2,
        expected_roll_dice_call_count: int = 1,
        expected_mock_get_max_move_count: int = 1,
        expected_move_call_count: int = 1,
        expected_extra_send_output_args: Optional[Tuple[Any, ...]] = None,
        winning_side: Side = Side.FIRST,
        move_by_turn_rolls: bool = False,
    ) -> None:
        send_output = Mock()
        run(self.receive_input, send_output, move_by_turn_rolls)

        self.assertEqual(mock_choice.call_count, 2)
        allowed_rolls_first = mock_choice.call_args_list[0].args[0]
        self.assertIsInstance(allowed_rolls_first, list)

        allowed_rolls_second = mock_choice.call_args_list[1].args[0]
        allowed_rolls_expected = list(
            roll
            for roll in range(1, DIE_FACE_COUNT + 1)
            if roll != DIE_ROLL_HIGH_EXAMPLE
        )
        self.assertEqual(allowed_rolls_second, allowed_rolls_expected)

        self.assertEqual(mock_send_state.call_count, expected_send_state_call_count)
        for call in mock_send_state.call_args_list:
            self.assertEqual(len(call.args), 1)
            self.assertIs(call.args[0], send_output)

        expected_send_output_args_list: List[Tuple[Any, ...]] = [
            (
                OutputType.TURN_ROLLS,
                DieRolls(DIE_ROLL_HIGH_EXAMPLE, DIE_ROLL_LOW_EXAMPLE),
            ),
            (OutputType.MOVE_ROLLS, DIE_ROLLS_EXAMPLE),
            (OutputType.GAME_WON, winning_side),
        ]
        if expected_extra_send_output_args is not None:
            expected_send_output_args_list.insert(2, expected_extra_send_output_args)
        if move_by_turn_rolls:
            del expected_send_output_args_list[1]
        self.assertEqual(send_output.call_count, len(expected_send_output_args_list))
        for call, expected_args in zip(
            send_output.call_args_list, expected_send_output_args_list
        ):
            self.assertEqual(call.args, expected_args)

        self.assertEqual(mock_roll_dice.call_count, expected_roll_dice_call_count)
        for call in mock_roll_dice.call_args_list:
            self.assertEqual(len(call.args), 1)
            self.assertIsInstance(call.args[0], Game)

        self.assertEqual(
            mock_get_max_move_count.call_count, expected_mock_get_max_move_count
        )
        mock_get_max_move_count.assert_called_with()

        self.assertEqual(mock_move.call_count, expected_move_call_count)
        mock_move.assert_called_with(*self.example_move)

    def test_move_not_none(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
        )

    def test_move_none(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.receive_input.side_effect = (InputType.MOVE, None), (
            InputType.MOVE,
            self.example_move,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_extra_send_output_args=(
                OutputType.INVALID_MOVE,
                InvalidMoveCode.INVALID_MOVE_TYPE,
                Side.FIRST,
            ),
        )

    def test_move_invalid(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        INVALID_MOVE_CODE = InvalidMoveCode.SOURCE_NOT_OWNED_PIECE
        mock_move.side_effect = (
            InvalidMove(INVALID_MOVE_CODE, self.example_move[0]),
            GameWon,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_move_call_count=2,
            expected_extra_send_output_args=(
                OutputType.INVALID_MOVE,
                INVALID_MOVE_CODE,
                Side.FIRST,
            ),
        )

    def test_move_two_pieces(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        mock_move.side_effect = (
            None,
            GameWon,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_send_state_call_count=3,
            expected_move_call_count=2,
        )

    def test_move_reach_max_count(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        mock_get_max_move_count.return_value = 1
        mock_move.side_effect = (
            None,
            GameWon,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            3,
            2,
            2,
            2,
            expected_extra_send_output_args=(OutputType.MOVE_ROLLS, DIE_ROLLS_EXAMPLE),
            winning_side=Side.SECOND,
        )

    def test_undo_not_none(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.receive_input.side_effect = (InputType.UNDO, 2), (
            InputType.MOVE,
            self.example_move,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_extra_send_output_args=(
                OutputType.INVALID_MOVE,
                InvalidMoveCode.INVALID_MOVE_TYPE,
                Side.FIRST,
            ),
        )

    def test_undo_empty_stack(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.receive_input.side_effect = (InputType.UNDO, None), (
            InputType.MOVE,
            self.example_move,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_extra_send_output_args=(
                OutputType.INVALID_MOVE,
                InvalidMoveCode.NOTHING_TO_UNDO,
                Side.FIRST,
            ),
        )

    def test_undo(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        mock_move.side_effect = (
            None,
            GameWon,
        )
        self.receive_input.side_effect = (
            (
                InputType.MOVE,
                self.example_move,
            ),
            (InputType.UNDO, None),
            (
                InputType.MOVE,
                self.example_move,
            ),
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_send_state_call_count=4,
            expected_move_call_count=2,
        )

    def test_invalid_input_type(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.receive_input.side_effect = (8, 2), (
            InputType.MOVE,
            self.example_move,
        )
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_extra_send_output_args=(
                OutputType.INVALID_MOVE,
                InvalidMoveCode.INVALID_INPUT_TYPE,
                Side.FIRST,
            ),
        )

    def test_move_by_turn_rolls(
        self,
        mock_move: Mock,
        mock_get_max_move_count: Mock,
        mock_roll_dice: Mock,
        mock_send_state: Mock,
        mock_choice: Mock,
    ) -> None:
        self.check_calls(
            mock_move,
            mock_get_max_move_count,
            mock_roll_dice,
            mock_send_state,
            mock_choice,
            expected_roll_dice_call_count=0,
            move_by_turn_rolls=True,
        )
