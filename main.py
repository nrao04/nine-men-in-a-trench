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