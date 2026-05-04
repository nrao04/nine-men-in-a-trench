import math
import queue
from collections import deque

# there are 13 spots total: (1..10 is the long trench & 11..13 are the three side pockets)
N = 13

def to_board(cells):
    # lists can change in place, but tuples cannot. search uses a set() of visited boards,
    # and tuples are hashable so they work inside that set.
    return tuple(cells)


def show(board):
    # simple print helper so the trace looks readable
    # first line = main trench only
    line_a = []
    for i in range(10):
        v = board[i]
        # 0 means empty square, letter b matches the old 8 puzzle blank printing style
        line_a.append("b" if v == 0 else str(v))
    # second line = the three pocket squares only
    line_b = []
    for i in range(10, 13):
        v = board[i]
        line_b.append("b" if v == 0 else str(v))
    print("Trench (1-10):", " ".join(line_a))
    print("Recesses (11-13):", " ".join(line_b))