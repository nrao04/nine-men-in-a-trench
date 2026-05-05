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

def shortest_steps_to_square1():
    # A* needs a cheap guess h(n), "Manhattan on the graph" idea:
    # real Manhattan needs rows/cols; here the trench is a weird shape so we use BFS
    # shortest_hops[index] == minimum edges from that cell down to square 1 (cell index 0)
    # -1 means "not visited yet in this BFS"
    shortest_hops = [-1] * NUM_BOARD_CELLS  
    # square 1 is distance 0 from itself
    shortest_hops[0] = 0  
    # breadth-first queue of cell indexes
    cells_waiting = deque([0])  

    while len(cells_waiting) > 0:
        # classic FIFO queue behavior for breadth-first
        current_cell = cells_waiting.popleft()  
        for neighbor_cell in NEIGHBORS[current_cell]:
            # first time we touch this neighbor we found shortest hop count in this tree-ish graph
            if shortest_hops[neighbor_cell] == -1:
                shortest_hops[neighbor_cell] = shortest_hops[current_cell] + 1
                cells_waiting.append(neighbor_cell)

    return shortest_hops

# build once at import time so the heuristic is just an array lookup later (fast)
# each slot answers: "how many moves along edges from this cell to square 1?"
DISTANCE_LOOKUP_TO_SQUARE1 = shortest_steps_to_square1()