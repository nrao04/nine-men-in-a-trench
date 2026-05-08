# CS205 - Nine Men in a Trench (Project 1)

## Overview

“Nine Men in a Trench” as a sliding puzzle on a fixed graph: nine numbered tiles, four blanks, trench + pockets. You can run Uniform Cost Search, `A*`, or Greedy best-first. Heuristic `h(n)` is precomputed shortest hop distance on the graph from wherever the sergeant (tile `1`) sits to square 1.

## How to run

From this folder:

```bash
python3 main.py
```

Follow the prompts: pick a preset or type your own 13-cell layout, then pick an algorithm (1–3).

If you use Conda, activate your env first, same command afterward.

## Code map

**Classes**

- `Problem` — start/goal, successor moves (slide a piece into an adjacent empty cell), heuristic `h_sergeant_to_square1`
- `Node` — board, `g(n)`, parent, last move label
- `Tree` — holds the root node; `Tree.path()` walks parents to recover the solution sequence

**Helpers / search**

- `to_board`, `show` — tuple state + console print  
- `NEIGHBORS` — adjacency list for all 13 cells  
- `shortest_steps_to_square1`, `DISTANCE_LOOKUP_TO_SQUARE1` — precomputed hop counts toward cell 1 (used for `h`)  
- `ucs`, `astar`, `greedy_best_first` — frontier search with traced expansions  
- `valid_board`, `read_board` — check/input a full board as 13 ints (`0` = empty)

**Driver**

- `main()` — menu presets, algorithm choice, goal stats and move sequence

## Presets

Three built-ins: solved goal layout, classic Dudeney-style start, and a one-move-from-goal sanity case. Custom boards are OK if they pass `valid_board` (four zeros, digits `1`–`9` each exactly once).

## Requirements

Python 3.x — stdlib only (`queue`, `collections`).