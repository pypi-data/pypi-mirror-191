from copy import deepcopy
from random import choice, randint
from typing import Callable, Optional, Set, Tuple, Union

from pygammon.exceptions import GameWon, InvalidMove, MaxMovesFound
from pygammon.structures import (
    BOARD_SIZE,
    DIE_FACE_COUNT,
    OUTSIDE_LENGTH,
    SIDE_PIECE_COUNT,
    Beginning,
    DieRolls,
    Direction,
    GameState,
    InputType,
    InvalidMoveCode,
    OutputType,
    OutsideStart,
    Player,
    Point,
    SendOutputCallable,
    Side,
    StartingCount,
)


class Game:
    """Game state and functionality"""

    def __init__(self, side: Side) -> None:
        """Initialize board and players.

        Args:
            side: The starting side
        """
        self.side = side
        self.dice_played: Set[int] = set()

        # Setup board
        self.board = [Point() for _ in range(BOARD_SIZE)]
        self.board[0] = Point(Side.SECOND, StartingCount.LOW)
        self.board[5] = Point(Side.FIRST, StartingCount.HIGH)
        self.board[7] = Point(Side.FIRST, StartingCount.MEDIUM)
        self.board[11] = Point(Side.SECOND, StartingCount.HIGH)
        self.board[12] = Point(Side.FIRST, StartingCount.HIGH)
        self.board[16] = Point(Side.SECOND, StartingCount.MEDIUM)
        self.board[18] = Point(Side.SECOND, StartingCount.HIGH)
        self.board[23] = Point(Side.FIRST, StartingCount.LOW)

        # Create players
        first_player = Player(Beginning.NORTH, Direction.DOWN, OutsideStart.LATE)
        second_player = Player(Beginning.SOUTH, Direction.UP, OutsideStart.EARLY)
        self.players = {Side.FIRST: first_player, Side.SECOND: second_player}

    def roll_dice(self) -> None:
        """Roll two dice and store the steps."""
        self.dice: Union[Tuple[int, int], Tuple[int, int, int, int]] = randint(
            1, DIE_FACE_COUNT
        ), randint(1, DIE_FACE_COUNT)

        # Check for doubles
        if self.dice[0] == self.dice[1]:
            self.dice *= 2

    def move(self, die_index: int, source: Optional[int]) -> None:
        """Attempt to make given move.

        Args:
            die_index: The die roll index to play
            source: The point to start the move from

        Raises:
            InvalidMove: On not allowed move attempt
            GameWon: On game being won
        """
        if die_index in self.dice_played:
            raise InvalidMove(InvalidMoveCode.DIE_INDEX_INVALID, die_index)

        try:
            step = self.dice[die_index]
        except IndexError:
            raise InvalidMove(InvalidMoveCode.DIE_INDEX_INVALID, die_index)

        player = self.players[self.side]

        if player.hit:
            if source is not None:
                raise InvalidMove(InvalidMoveCode.SOURCE_INVALID, source)

            source = player.beginning
        else:
            if source is None:
                raise InvalidMove(InvalidMoveCode.SOURCE_INVALID, source)

            try:
                source_point = self.board[source]
            except IndexError:
                raise InvalidMove(InvalidMoveCode.SOURCE_INVALID, source)

            if source_point.side is not self.side:
                raise InvalidMove(InvalidMoveCode.SOURCE_NOT_OWNED_PIECE, source)

        destination = source + step * player.direction

        if 0 <= destination < BOARD_SIZE:
            destination_point = self.board[destination]

            if destination_point.side is None or destination_point.side is self.side:
                # Simply move
                destination_point.count += 1
            else:
                if destination_point.count > 1:
                    # Occupied
                    raise InvalidMove(InvalidMoveCode.DESTINATION_OCCUPIED, destination)

                # Hit opponent
                self.players[Side(not self.side)].hit += 1

            destination_point.side = self.side

        else:
            # Check if bearing off is possible
            bearing_off = True
            for point in self.board[
                player.outside_start : player.outside_start + OUTSIDE_LENGTH
            ]:
                if point.side is self.side:
                    bearing_off = False
                    break

            if bearing_off:
                player.borne += 1
            else:
                raise InvalidMove(InvalidMoveCode.DESTINATION_OUT_OF_BOARD, destination)

        if player.hit:
            player.hit -= 1
        else:
            # Remove piece from source
            source_point.count -= 1
            if not source_point.count:
                source_point.side = None

        self.dice_played.add(die_index)

        if player.borne == SIDE_PIECE_COUNT:
            raise GameWon

    def _add_move_count(
        self, die_index: int, source: Optional[int], move_counts: Set[int]
    ) -> None:
        """Add possible move count to given set, after attempting to make given move.

        Args:
            die_index: The die roll index to play
            source: The point to start the move from
            move_counts: The set to add the move count to
        """
        try:
            self.move(die_index, source)
        except InvalidMove:
            pass
        except GameWon:
            move_counts.add(1)
        else:
            move_counts.add(1 + self._get_move_count())

    def _get_move_count(self) -> int:
        """Get possible move count, for current state.

        Returns:
            The possible move count

        Raises:
            MaxMovesFound: On max possible moves found
        """
        if len(self.dice_played) == len(self.dice):
            raise MaxMovesFound

        game = deepcopy(self)
        move_counts: Set[int] = set()

        for die_index in range(len(game.dice)):
            if game.players[game.side].hit:
                game._add_move_count(die_index, None, move_counts)
            else:
                for source in range(BOARD_SIZE):
                    game._add_move_count(die_index, source, move_counts)

        return max(move_counts) if move_counts else 0

    def get_max_move_count(self) -> int:
        """Get max possible move count, for current state.

        Returns:
            The max possible move count
        """
        try:
            return self._get_move_count()
        except MaxMovesFound:
            return len(self.dice)

    def send_state(self, send_output: SendOutputCallable) -> None:
        """Send player output about the game state.

        Args:
            send_output: Callable sending player output
        """
        first_player = self.players[Side.FIRST]
        second_player = self.players[Side.SECOND]
        game_state = GameState(
            self.board,
            first_player.hit,
            first_player.borne,
            second_player.hit,
            second_player.borne,
        )
        send_output(OutputType.GAME_STATE, game_state)


def run(
    receive_input: Callable[
        [Side], Tuple[InputType, Optional[Tuple[int, Optional[int]]]]
    ],
    send_output: SendOutputCallable,
    move_by_turn_rolls: bool = False,
) -> None:
    """Start a game, using given callables for player input and output.

    Args:
        receive_input: Callable receiving player input
        send_output: Callable sending player output
    """
    allowed_rolls = list(range(1, DIE_FACE_COUNT + 1))

    # Make turns rolls
    first_roll = choice(allowed_rolls)
    allowed_rolls.remove(first_roll)
    second_roll = choice(allowed_rolls)

    side = Side.FIRST if first_roll > second_roll else Side.SECOND
    game = Game(side)

    game.send_state(send_output)
    send_output(OutputType.TURN_ROLLS, DieRolls(first_roll, second_roll))

    while True:
        if move_by_turn_rolls:
            game.dice = first_roll, second_roll
            move_by_turn_rolls = False
        else:
            game.roll_dice()
            rolls = game.dice[:2]
            send_output(OutputType.MOVE_ROLLS, DieRolls(*rolls))

        game_states = []
        move_count = 0
        max_move_count = game.get_max_move_count()

        while move_count < max_move_count:
            input_type, move = receive_input(game.side)

            if input_type is InputType.MOVE:
                if move is None:
                    send_output(
                        OutputType.INVALID_MOVE,
                        InvalidMoveCode.INVALID_MOVE_TYPE,
                        game.side,
                    )
                    continue

                backup_game = deepcopy(game)

                try:
                    game.move(*move)
                except InvalidMove as exc:
                    send_output(OutputType.INVALID_MOVE, exc.code, game.side)
                    game = backup_game
                except GameWon:
                    game.send_state(send_output)
                    send_output(OutputType.GAME_WON, game.side)
                    return
                else:
                    # Valid move, game continues
                    game_states.append(backup_game)
                    move_count += 1
                    game.send_state(send_output)

            elif input_type is InputType.UNDO:
                if move is not None:
                    send_output(
                        OutputType.INVALID_MOVE,
                        InvalidMoveCode.INVALID_MOVE_TYPE,
                        game.side,
                    )
                    continue

                # Try to undo
                try:
                    game = game_states.pop()
                except IndexError:
                    send_output(
                        OutputType.INVALID_MOVE,
                        InvalidMoveCode.NOTHING_TO_UNDO,
                        game.side,
                    )
                else:
                    move_count -= 1
                    game.send_state(send_output)

            else:
                send_output(  # type: ignore[unreachable]
                    OutputType.INVALID_MOVE,
                    InvalidMoveCode.INVALID_INPUT_TYPE,
                    game.side,
                )

        game.side = Side(not game.side)
        game.dice_played = set()
