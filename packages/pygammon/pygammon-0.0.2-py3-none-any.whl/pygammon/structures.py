from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import List, NamedTuple, Optional, Protocol, Tuple, Union

BOARD_SIZE = 24
DIE_FACE_COUNT = 6
OUTSIDE_LENGTH = 18
SIDE_PIECE_COUNT = 15


class Side(IntEnum):
    """Playing side"""

    FIRST = 0
    SECOND = 1


class StartingCount(IntEnum):
    """Starting piece count of some point"""

    LOW = 2
    MEDIUM = 3
    HIGH = 5


class Beginning(IntEnum):
    """Index for hit pieces to start from"""

    NORTH = BOARD_SIZE
    SOUTH = -1


class Direction(IntEnum):
    """Moving direction"""

    DOWN = -1
    UP = 1


class OutsideStart(IntEnum):
    """Starting point of non-bearing area"""

    LATE = 6
    EARLY = 0


class InvalidMoveCode(Enum):
    """Invalid move error codes"""

    DIE_INDEX_INVALID = 0
    SOURCE_INVALID = 1
    SOURCE_NOT_OWNED_PIECE = 2
    DESTINATION_OUT_OF_BOARD = 3
    DESTINATION_OCCUPIED = 4
    INVALID_MOVE_TYPE = 5
    NOTHING_TO_UNDO = 6
    INVALID_INPUT_TYPE = 7


class InputType(Enum):
    """Reason to receive input"""

    MOVE = 0
    UNDO = 1


class OutputType(Enum):
    """Reason to send output"""

    GAME_STATE = 0
    TURN_ROLLS = 1
    MOVE_ROLLS = 2
    INVALID_MOVE = 3
    GAME_WON = 4


@dataclass
class Point:
    """Board point data"""

    side: Optional[Side] = None
    count: int = 0


@dataclass
class Player:
    """Player data"""

    beginning: int
    direction: Direction
    outside_start: OutsideStart
    hit: int = 0
    borne: int = 0


class GameState(NamedTuple):
    """Game state data"""

    board: List[Point]
    """The game board"""

    first_hit: int
    """Count of first player's pieces that have been hit"""

    first_borne: int
    """Count of pieces first player has borne off"""

    second_hit: int
    """Count of second player's pieces that have been hit"""

    second_borne: int
    """Count of pieces second player has borne off"""


class DieRolls(NamedTuple):
    """Two die rolls"""

    first: int
    """First die roll"""

    second: int
    """Second die roll"""


class SendOutputCallable(Protocol):
    def __call__(
        self,
        output_type: OutputType,
        data: Union[GameState, Tuple[int, int], InvalidMoveCode, Side],
        /,
        side: Optional[Side] = None,
    ) -> None:
        ...  # pragma: no cover
