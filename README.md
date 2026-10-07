# Battle-IA — Ultimate Tic-Tac-Toe

A Python console game with a search-based AI opponent using **Minimax and alpha-beta pruning**.

## Context and objective

Academic AI project exploring decision-making in Ultimate Tic-Tac-Toe. Student teams developed agents that were confronted with one another. This repository provides a human-versus-AI console implementation.

## Method

- `GameState` stores the board, local-board results, current player and next playable board.
- Minimax searches possible game states; alpha-beta pruning avoids branches that cannot improve the current decision.
- A heuristic evaluates local and global positions.
- Move ordering prioritises local wins, centres and corners.
- The console game uses a search depth of **6**. Thinking time depends on the position and machine.

This is a search-based AI: it does not train a machine learning model.

## Technologies

Python 3 and the standard library (`random`, `time`). No external dependencies are required.

## Project structure

```text
ultimate_tic_tac_toe.py   # Rules, game state, search and console interface
.gitignore
README.md
```

## How to run

From the repository directory:

```sh
python ultimate_tic_tac_toe.py
```

Choose `1` for the human to start or `2` for the AI. The human plays `X`, the AI plays `O`. Enter the **column first, then the row**, both between 1 and 9. Console prompts are in French.

## Rules

The board contains nine smaller tic-tac-toe boards. Your position within a small board determines the board where your opponent must play next. If that destination board has already ended, the opponent can play on any open board. Win three local boards in a row to win the game.

## Current status

The repository contains the console game and AI implementation. No tournament ranking, benchmark or win-rate claim is made. Search time can grow substantially in open positions.

## Possible future improvements

- Add tests for legal moves, terminal states and undo operations.
- Benchmark search time on a fixed set of positions.
- Compare heuristics and consider iterative deepening with a time limit.

These are proposed extensions, not implemented features.
