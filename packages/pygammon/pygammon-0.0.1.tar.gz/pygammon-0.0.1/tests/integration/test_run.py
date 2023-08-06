import unittest
from copy import deepcopy
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union, cast
from unittest.mock import Mock, call, patch

from pygammon.core import run
from pygammon.structures import (
    BOARD_SIZE,
    DieRolls,
    GameState,
    InputType,
    InvalidMoveCode,
    OutputType,
    Point,
    Side,
    StartingCount,
)


class CopyingMock(Mock):
    def __call__(self, *args: Any, **kwargs: Any) -> "CopyingMock":
        return cast(CopyingMock, super().__call__(*deepcopy(args), **deepcopy(kwargs)))


class TestRun(unittest.TestCase):
    @patch("pygammon.core.choice")
    @patch("pygammon.core.randint")
    def test_run(self, mock_randint: Mock, mock_choice: Mock) -> None:
        board = [Point() for _ in range(BOARD_SIZE)]
        board[0] = Point(Side.SECOND, StartingCount.LOW)
        board[5] = Point(Side.FIRST, StartingCount.HIGH)
        board[7] = Point(Side.FIRST, StartingCount.MEDIUM)
        board[11] = Point(Side.SECOND, StartingCount.HIGH)
        board[12] = Point(Side.FIRST, StartingCount.HIGH)
        board[16] = Point(Side.SECOND, StartingCount.MEDIUM)
        board[18] = Point(Side.SECOND, StartingCount.HIGH)
        board[23] = Point(Side.FIRST, StartingCount.LOW)
        game_state = GameState(board, 0, 0, 0, 0)

        attr_names = {
            "fh": "first_hit",
            "fb": "first_borne",
            "sh": "second_hit",
            "sb": "second_borne",
        }

        expected_calls = []
        choice_results: List[int] = []
        randint_results: List[int] = []
        receive_input_results = []

        fixture_path = Path(__file__).parent / "fixtures/game"
        contents = fixture_path.read_text().splitlines()
        for line in filter(None, contents):
            if line[0] == "c":
                choice_results.extend(int(roll) for roll in line[2:].split())
            elif line[0] == "d":
                randint_results.extend(int(roll) for roll in line[2:].split())
            elif line[0] == "i":
                parts = line[2:].split()
                results: List[Optional[Union[InputType, Tuple[int, Optional[int]]]]] = [
                    InputType(int(parts[0]))
                ]
                if len(parts) == 2:
                    results.append(None)
                else:
                    results.append(
                        cast(
                            Tuple[int, Optional[int]],
                            tuple(
                                None if part == "n" else int(part) for part in parts[1:]
                            ),
                        )
                    )
                receive_input_results.append(tuple(results))
            elif line[0] == "r":
                side = Side(int(line[2]))
                expected_calls.append(call.receive_input(side))
            elif line[0] == "s":
                args: List[
                    Union[OutputType, GameState, DieRolls, InvalidMoveCode, Side]
                ] = [OutputType(int(line[2]))]
                tuple_args = []

                for part in line[4:].split():
                    if part == "g":
                        args.append(deepcopy(game_state))
                    elif part[0] == "c":
                        args.append(InvalidMoveCode(int(part[1])))
                    elif part[0] == "s":
                        args.append(Side(int(part[1])))
                    else:
                        tuple_args.append(int(part))
                if tuple_args:
                    args.insert(1, DieRolls(*tuple_args))

                expected_calls.append(call.send_output(*args))
            else:
                for part in line.split():
                    try:
                        attr_name = attr_names[part[:2]]
                    except KeyError:
                        index, count, side_symbol = part.split(",")
                        point_side: Optional[Side] = (
                            None if side_symbol == "n" else Side(int(side_symbol))
                        )
                        board[int(index)] = Point(point_side, int(count))
                    else:
                        game_state_kwargs = {
                            name: getattr(game_state, name)
                            for name in ["board", *attr_names.values()]
                        }
                        game_state_kwargs[attr_name] = int(part[2:])
                        game_state = GameState(**game_state_kwargs)

        mock_choice.side_effect = choice_results
        mock_randint.side_effect = randint_results

        mock = CopyingMock()
        mock.receive_input = CopyingMock(side_effect=receive_input_results)

        run(mock.receive_input, mock.send_output)

        self.assertEqual(mock.mock_calls, expected_calls)
        self.assertEqual(mock_choice.call_count, len(choice_results))
        self.assertEqual(mock_randint.call_count, len(randint_results))
