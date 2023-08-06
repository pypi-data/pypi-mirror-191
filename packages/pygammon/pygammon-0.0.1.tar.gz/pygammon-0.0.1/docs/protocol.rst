Protocol
========

Game loop
---------

The :func:`~pygammon.run` function uses its arguments, the `receive_input` and `send_output` callables,
to get player moves and send game-related info, respectively.

The former takes a :class:`~pygammon.Side` as its argument, stating which side is expecting input from.
It should return a 2-tuple of:

    - an :class:`~pygammon.InputType`, indicating the input's purpose
    - a 2-tuple of (or ``None`` under circumstances):

        - an ``int``
        - an ``int`` (or ``None`` under circumstances)

The latter takes an :class:`~pygammon.OutputType` as its first argument, indicating the output's purpose.
Its second argument is the data, which can be a :class:`~pygammon.GameState`, a tuple of 2 ``int``s,
an :class:`~pygammon.InvalidMoveCode`, or a :class:`~pygammon.Side`. It can optionally take a third argument,
a :class:`~pygammon.Side`, indicating which side the output is addressed to. If the third argument is ommited
(should have a ``None`` default value), the output concerns both sides.

- Once the game starts, `send_output` sends the initial game state: the :attr:`OutputType.GAME_STATE <pygammon.OutputType.GAME_STATE>`
  constant, and a :class:`~pygammon.GameState` instance.
- Then, it sends the turn-deciding die rolls: the :attr:`OutputType.TURN_ROLLS <pygammon.OutputType.TURN_ROLLS>` constant, and a
  :class:`~pygammon.structures.DieRolls` instance.
- Then, the game loop starts:

    - The dice are rolled and both sides get informed by `send_output` with: the :attr:`OutputType.MOVE_ROLLS <pygammon.OutputType.MOVE_ROLLS>`
      constant, and a :class:`~pygammon.structures.DieRolls` instance.
    - Then, until a valid move is made, or game is won:

        - `receive_input` is called with the currently playing :class:`~pygammon.Side`.
        - If the first item of its results is :attr:`InputType.MOVE <pygammon.InputType.MOVE>`:

            - If the second item is ``None``, `send_output` sends :attr:`OutputType.INVALID_MOVE <pygammon.OutputType.INVALID_MOVE>`,
              :attr:`InvalidMoveCode.INVALID_MOVE_TYPE <pygammon.InvalidMoveCode.INVALID_MOVE_TYPE>`, and the current :class:`~pygammon.Side`.
            - Else, it tries to :ref:`make the given move <moving>`.

                - If it is invalid, `send_output` sends :attr:`OutputType.INVALID_MOVE <pygammon.OutputType.INVALID_MOVE>`,
                  an :class:`~pygammon.InvalidMoveCode`, and the current :class:`~pygammon.Side`.
                - Else, the move is made.

                    - If game is won, `send_output` sends :attr:`OutputType.GAME_STATE <pygammon.OutputType.GAME_STATE>`,
                      and a :class:`~pygammon.GameState` instance. Then, it is called once more with :attr:`OutputType.GAME_WON
                      <pygammon.OutputType.GAME_WON>`. The game loop terminates.
                    - Else, if all the moves have been made for this turn, `send_output` sends :attr:`OutputType.GAME_STATE
                      <pygammon.OutputType.GAME_STATE>`, and a :class:`~pygammon.GameState` instance, and the other side starts their turn.

        - Else (the first item should be :attr:`InputType.UNDO <pygammon.InputType.UNDO>`):

            - If the second item is not ``None``, `send_output` sends :attr:`OutputType.INVALID_MOVE <pygammon.OutputType.INVALID_MOVE>`,
              :attr:`InvalidMoveCode.INVALID_MOVE_TYPE <pygammon.InvalidMoveCode.INVALID_MOVE_TYPE>`, and the current :class:`~pygammon.Side`.
            - Else, if there are no moves to undo, `send_output` sends :attr:`OutputType.INVALID_MOVE <pygammon.OutputType.INVALID_MOVE>`,
              :attr:`InvalidMoveCode.NOTHING_TO_UNDO <pygammon.InvalidMoveCode.NOTHING_TO_UNDO>`, and the current :class:`~pygammon.Side`.
            - Else, the last move is undone.

.. _moving:

Moving
------

The board's points are indexed from bottom right to bottom left, then top left to top right. The first player's base is the bottom right quarter.

The move data should be a 2-tuple, consisting of:

    - the index of the die that is intended to be played, considering the order of the die rolls as they were sent by the game
    - the index on the board, of the piece to be moved (from `source` to `desitnation`), or ``None`` if player has pieces that have been hit

In case the move is invalid, `send_output` is called with :attr:`OutputType.INVALID_MOVE <pygammon.OutputType.INVALID_MOVE>`, an
:class:`~pygammon.InvalidMoveCode`, and the current :class:`~pygammon.Side`. Below is described which codes are sent in which cases:

- :attr:`InvalidMoveCode.DIE_INDEX_INVALID <pygammon.InvalidMoveCode.DIE_INDEX_INVALID>`

    - Die index is already played
    - Die index does not exist

- :attr:`InvalidMoveCode.SOURCE_INVALID <pygammon.InvalidMoveCode.SOURCE_INVALID>`

    - Player has pieces that have been hit and source index is not ``None``
    - Player does not have pieces that have been hit and source index is ``None``
    - Source index does not exist

- :attr:`InvalidMoveCode.SOURCE_NOT_OWNED_PIECE <pygammon.InvalidMoveCode.SOURCE_NOT_OWNED_PIECE>`

    - Source is not a piece belonging to the player

- :attr:`InvalidMoveCode.DESTINATION_OCCUPIED <pygammon.InvalidMoveCode.DESTINATION_OCCUPIED>`

    - Destination is occupied by two ore more opponent pieces

- :attr:`InvalidMoveCode.DESTINATION_OUT_OF_BOARD <pygammon.InvalidMoveCode.DESTINATION_OUT_OF_BOARD>`

    - Player is not bearing off and destination is out of the board
