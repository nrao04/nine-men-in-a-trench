import math
import queue
from collections import deque

# there are 13 spots total: (1..10 is the long trench & 11..13 are the three side pockets)
NUM_BOARD_CELLS = 13

# helper functions for the puzzle

def to_board(cells):
    # lists can change in place, but tuples cannot. search uses a set() of visited boards,
    # and tuples are hashable so they work inside that set.
    return tuple(cells)


def show(board):
    # simple print helper so the trace looks readable
    # first line = main trench only
    trench_symbols = []
    for cell_index in range(10):
        cell_value = board[cell_index]
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
# list index is python cell id (0-based), so each inner list is other cells you can walk to in 1 move.
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
    # real Manhattan needs rows/cols, here the trench is a weird shape so we use BFS
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

class Problem:
    # prob. class bundles everything specific to trench puzzle:
    # (start layout, goal layout, successor generator, & heuristic wrapper)

    def __init__(self, initial_state, goal_state):
        # store immutable tuples because search compares states and hashes them
        self.initial_state = to_board(initial_state)
        self.goal_state = to_board(goal_state)

    def is_goal(self, board):
        # goal test from pseudocode: literally compare full states
        return board == self.goal_state
    
    def neighbors(self, board):
        # same swap trick here except neighbors come from NEIGHBORS[] instead of grid math
        # we iterate every empty slot on the board (there are four zeros total).
        # each adjacent numbered man can slide into that empty -> one new board state.
        for empty_cell_index in range(NUM_BOARD_CELLS):
            if board[empty_cell_index] != 0:
                continue  # not blank; skip
            for neighbor_cell_index in NEIGHBORS[empty_cell_index]:
                neighbor_piece = board[neighbor_cell_index]
                if neighbor_piece == 0:
                    continue  # neighbor is also empty -> no tile to push into blank

                # copy into a fresh list so we do not mutate the parent board by accident
                next_board_list = list(board)
                # swap blank square with chosen man -> he lands on empty_cell_index
                next_board_list[empty_cell_index], next_board_list[neighbor_cell_index] = (
                    next_board_list[neighbor_cell_index],
                    next_board_list[empty_cell_index],
                )

                # edge label for debugging & printing solution path
                # numbers shown as worksheet positions (add +1 because Python indexes from 0)
                move_label = str(neighbor_cell_index + 1) + "->" + str(empty_cell_index + 1)
                yield to_board(next_board_list), move_label
    
    def h_sergeant_to_square1(self, board):
        # Heuristic h(n): estimate moves needed focusing on the sergeant (piece labeled 1).
        # DISTANCE_LOOKUP_TO_SQUARE1 tells how many edges away each square is from square 1.
        # scan for wherever token 1 sits and read off that distance table entry.
        for cell_index in range(NUM_BOARD_CELLS):
            if board[cell_index] == 1:
                return DISTANCE_LOOKUP_TO_SQUARE1[cell_index]
        # puzzle definition guarantees man 1 exists, so this line is just defensive coding
        return math.inf
    
class Node:
    # mirrors the old eight puzzle Node idea:
    # board -> current layout
    # cost -> depth / path cost g(n) counted as number of moves so far
    # parent -> who spawned this node so we can reconstruct actions later
    # action -> last edge label from parent -> child

    def __init__(self, board, cost, parent, action):
        self.board = board
        self.cost = cost  # g(n)
        self.parent = parent
        self.action = action
        
class Tree:
    # creating a wrapper here so ucs & astar read better like sample driver code
    def __init__(self, root_board):
        # root has cost zero and no parent yet
        self.root = Node(root_board, 0, None, "")

    # helper function to get the path from the goal node to the root node
    @staticmethod
    def path(goal_node):
        # rebuilding solution sequence by crawling parents from goal back toward root
        steps = []
        trace_node = goal_node
        while trace_node is not None and trace_node.action != "":
            # append the action to the steps list
            steps.append(trace_node.action)
            trace_node = trace_node.parent
        # walking backwards puts moves newest-first, assignment wants start -> goal order
        steps.reverse()
        return steps

# print helper funct. to avoid duplicate code
# (going to impl. search alg. later)
def print_step(node, path_cost, heuristic_value=None, greedy_tag=False):
    # UCS passes no heuristic -> heuristic_value stays None.
    # A* passes real h(n).
    # greedy_tag tweaks wording because greedy ranks nodes differently than A*
    # print the step with the path cost and heuristic value
    if greedy_tag and path_cost == 0:
        print("Expanding state (Greedy: only looks at h)")
    # if the greedy tag is true, print the best greedy state with the path cost and heuristic value
    elif greedy_tag:
        print(
            "The best Greedy state with g(n) = "
            + str(path_cost)
            + " and h(n) = "
            + str(heuristic_value)
            + " is..."
        )
    elif path_cost == 0:
        print("Expanding state")  # starting board print matches textbook trace examples
    elif heuristic_value is None:
        print("The best state to expand with g(n) = " + str(path_cost) + " is...")
    else:
        print(
            "The best state to expand with g(n) = "
            + str(path_cost)
            + " and h(n) = "
            + str(heuristic_value)
            + " is..."
        )
    show(node.board)
    # first expansion usually skips this extra line so output mirrors Keogh sample traces
    if path_cost != 0:
        print("Expanding this node...")
        

def ucs(problem):
    # uniform cost -> always pop the node with smallest g first
    # (identical to A* if you forced h=0 every time)
    # priority tuple is (g, counter, node) so smaller g leaves the queue first

    frontier = queue.PriorityQueue()
    tie_breaker = 0
    # python breaks priority ties by comparing the next tuple item, so pure ints avoid TypeError
    # we bump tie_breaker so two equal priorities never try to compare Node objects

    start_node = Tree(problem.initial_state).root
    frontier.put((0, tie_breaker, start_node))

    explored = set()  # closed set / visited list
    expanded_count = 0
    max_queue_size = 1  # project handout sometimes wants "max nodes in queue" stat

    # while the frontier is not empty, get the best partial path
    while not frontier.empty():
        # pop best partial path
        uniform_cost_priority, tie_counter, current_node = frontier.get()  

        if current_node.board in explored:
            continue  # already fully processed this board layout
        explored.add(current_node.board)

        print_step(current_node, uniform_cost_priority)
        
        # if the current node is the goal, return the path cost, the expanded count, the max queue size, the current node cost, and the path from the goal node to the root node
        if problem.is_goal(current_node.board):
            return True, expanded_count, max_queue_size, current_node.cost, Tree.path(current_node)

        expanded_count += 1
        child_path_cost = current_node.cost + 1  # every operator costs exactly one hop here

        # for each successor board, add the board to the frontier
        for successor_board, move_label in problem.neighbors(current_node.board):
            # referencing eight puzzle driver logic, skip pushing duplicates already expanded
            if successor_board not in explored:
                tie_breaker += 1
                frontier.put(
                    (child_path_cost, tie_breaker, Node(successor_board, child_path_cost, current_node, move_label))
                )

        max_queue_size = max(max_queue_size, frontier.qsize())

    return False, expanded_count, max_queue_size, None, []

def astar(problem, heuristic):
    # classic A* from slides: f(n) = g(n) + h(n)
    #   g = real steps taken
    #   h = our guess (here: how many graph edges the sergeant still needs)
    # queue orders by f so hopefully we hit the goal after fewer expansions than raw UCS
    # tuple layout matches the class example: (f, g, tie, node) so we still know g when printing

    frontier = queue.PriorityQueue()
    tie_breaker = 0

    start_node = Tree(problem.initial_state).root
    # at the start, g=0 so f(0) = 0 + h(start) == h(start)
    frontier.put((heuristic(start_node.board), 0, tie_breaker, start_node))

    explored = set()
    expanded_count = 0
    max_queue_size = 1

    # while the frontier is not empty, get the best partial path
    while not frontier.empty():
        astar_priority_f, path_cost_so_far, tie_counter, current_node = frontier.get()  # lowest f first

        if current_node.board in explored:
            continue
        explored.add(current_node.board)

        # get the heuristic value at the current node
        heuristic_at_node = heuristic(current_node.board)  # recompute h for the trace printout
        _print_step(current_node, path_cost_so_far, heuristic_at_node)

        if problem.is_goal(current_node.board):
            return True, expanded_count, max_queue_size, current_node.cost, Tree.path(current_node)

        expanded_count += 1
        child_path_cost = current_node.cost + 1

        # for each successor board, add the board to the frontier
        for successor_board, move_label in problem.neighbors(current_node.board):
            if successor_board in explored:
                continue
            # create a new node with the successor board, the child path cost, the current node, and the move label
            child_node = Node(successor_board, child_path_cost, current_node, move_label)
            tie_breaker += 1
            # add the node to the frontier
            total_estimated_cost = child_path_cost + heuristic(child_node.board)  # child g + child h
            frontier.put((total_estimated_cost, child_path_cost, tie_breaker, child_node))

        max_queue_size = max(max_queue_size, frontier.qsize())

    return False, expanded_count, max_queue_size, None, []

