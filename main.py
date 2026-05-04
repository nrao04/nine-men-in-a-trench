import math
import queue
from collections import deque

# there are 13 spots total: (1..10 is the long trench & 11..13 are the three side pockets)
NUM_BOARD_CELLS = 13

def to_board(cells):
    # lists can change in place, but tuples cannot. search uses a set() of visited boards,
    # and tuples are hashable so they work inside that set.
    return tuple(cells)


def show(board):
    # simple print helper so the trace looks readable
    # first line = main trench only
    trench_symbols = []
    for cell_index in range(10):
        cell_value = board[i]
        # 0 means empty square, letter b matches the old 8 puzzle blank printing style
        trench_symbols.append("b" if cell_value == 0 else str(cell_value))
    # second line = the three pocket squares only
    pocket_symbols = []
    for cell_index in range(10, 13):
        v = board[cell_index]
        pocket_symbols.append("b" if cell_value == 0 else str(cell_value))
    print("Trench (1-10):", " ".join(trench_symbols))
    print("Recesses (11-13):", " ".join(pocket_symbols))

# static map of the trench + pockets.
# list index == python cell id (0-based), each inner list is other cells you can walk to in 1 move.
# we hardcode the graph so the reader sees the map without running any setup code.
# (one graph edge = one action in the search tree)
NEIGHBORS = [
    [1],  # pos 1  -> 2
    [0, 2],  # pos 2  -> 1,3
    [1, 3],  # pos 3  -> 2,4
    [2, 4, 10],  # pos 4  -> 3,5, and pocket 11
    [3, 5],  # pos 5  -> 4,6
    [4, 6, 11],  # pos 6  -> 5,7, and pocket 12
    [5, 7],  # pos 7  -> 6,8
    [6, 8, 12],  # pos 8  -> 7,9, and pocket 13
    [7, 9],  # pos 9  -> 8,10
    [8],  # pos 10 -> 9
    [3],  # pos 11 (pocket) -> only 4
    [5],  # pos 12 (pocket) -> only 6
    [7],  # pos 13 (pocket) -> only 8
]