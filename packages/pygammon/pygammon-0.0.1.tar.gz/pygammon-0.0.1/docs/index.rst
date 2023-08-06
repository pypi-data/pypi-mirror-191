pygammon
========

Backgammon engine core
----------------------

*pygammon* is the base of a `backgammon <https://en.wikipedia.org/wiki/Backgammon>`_ engine,
written in Python. It provides the core functionality for running a game, given a source of
input (player moves) and a destination for output (game state/events).

Installation
------------

The following Python versions are supported:

    - CPython: 3.8, 3.9, 3.10, 3.11, 3.12
    - PyPy: 3.8

- Install via `pip <https://packaging.python.org/tutorials/installing-packages/>`_:

.. code-block:: bash

   $ pip install pygammon

Usage
-----

To build a complete game, you have to provide a function for getting each side's moves (input),
and a function for informing each side about the game state and events (output):

.. code-block:: python

   from typing import Optional, Tuple, Union

   from pygammon import GameState, InputType, InvalidMoveCode, OutputType, Side, run


   def receive_input(side: Side) -> Tuple[InputType, Optional[Tuple[int, Optional[int]]]]:
       # Return move of given side
       ...


   def send_output(
       output_type: OutputType,
       data: Union[GameState, Tuple[int, int], InvalidMoveCode, Side],
       side: Optional[Side] = None,
   ) -> None:
       # Show output to given side
       ...


   run(receive_input, send_output)

The input function could send to the game, moves made in any way (calculated by AI, read from stdin,
selected from GUI, either locally or through network). Similarly, the output function could do anything
with the info it gets from the game (inform AI tactics, write to stdout, show to GUI, either locally or
through network).

For more details, see the :doc:`protocol <protocol>`.

License
-------

Distributed under the `MIT License <https://github.com/amikrop/pygammon/blob/master/LICENSE>`_.

.. toctree::
   :maxdepth: 1
   :caption: Contents
   :hidden:

   protocol
   interface
