from dataclasses import dataclass
from typing import Optional

from pygammon.structures import InvalidMoveCode


@dataclass(frozen=True)
class InvalidMove(Exception):
    """Attempt for invalid move"""

    code: InvalidMoveCode
    data: Optional[int]


class GameWon(Exception):
    """Game is won"""


class MaxMovesFound(Exception):
    """Max possible moves found"""
