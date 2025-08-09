# Rock-Paper-Scissors (CLI)

A simple Python command-line Rock-Paper-Scissors game with both interactive and one-shot modes.

## Requirements
- Python 3.9+

## Quick start
Interactive play:

```bash
python3 /workspace/rock_paper_scissors.py
```

Interactive best-of series (first to 3 in best-of-5):

```bash
python3 /workspace/rock_paper_scissors.py --best-of 5
```

One-shot round (non-interactive), with deterministic computer choice using a seed:

```bash
python3 /workspace/rock_paper_scissors.py --player rock --seed 42
```

Accepted choices: `rock`/`r`, `paper`/`p`, `scissors`/`s`.
