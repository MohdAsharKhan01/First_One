#!/usr/bin/env python3

import argparse
import random
from enum import Enum
from typing import Dict, Tuple


class Choice(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


VALID_INPUT_ALIASES: Dict[str, Choice] = {
    "r": Choice.ROCK,
    "rock": Choice.ROCK,
    "p": Choice.PAPER,
    "paper": Choice.PAPER,
    "s": Choice.SCISSORS,
    "scissors": Choice.SCISSORS,
}


def parse_choice(text: str) -> Choice:
    lowered = text.strip().lower()
    if lowered not in VALID_INPUT_ALIASES:
        raise ValueError(
            f"Invalid choice '{text}'. Valid options: rock(r), paper(p), scissors(s)"
        )
    return VALID_INPUT_ALIASES[lowered]


def determine_winner(player: Choice, computer: Choice) -> str:
    if player == computer:
        return "tie"
    wins_against = {
        Choice.ROCK: Choice.SCISSORS,
        Choice.PAPER: Choice.ROCK,
        Choice.SCISSORS: Choice.PAPER,
    }
    return "player" if wins_against[player] == computer else "computer"


def computer_pick(rng: random.Random) -> Choice:
    return rng.choice([Choice.ROCK, Choice.PAPER, Choice.SCISSORS])


def play_one_round(player_choice: Choice, rng: random.Random) -> Tuple[str, Choice]:
    cpu_choice = computer_pick(rng)
    result = determine_winner(player_choice, cpu_choice)
    return result, cpu_choice


def interactive_loop(rng: random.Random, best_of: int | None = None) -> int:
    player_wins = 0
    computer_wins = 0
    ties = 0

    rounds_needed_to_win = None
    total_rounds_limit = None
    if best_of is not None:
        if best_of <= 0 or best_of % 2 == 0:
            raise ValueError("--best-of must be a positive odd integer, e.g., 3, 5, 7")
        rounds_needed_to_win = best_of // 2 + 1
        total_rounds_limit = best_of
        print(f"Playing best-of {best_of}. First to {rounds_needed_to_win} wins.")

    print("Enter your move: rock (r), paper (p), scissors (s). Type 'q' to quit.")

    rounds_played = 0
    while True:
        if total_rounds_limit is not None and rounds_played >= total_rounds_limit:
            break
        if rounds_needed_to_win is not None and (
            player_wins >= rounds_needed_to_win or computer_wins >= rounds_needed_to_win
        ):
            break

        try:
            user_input = input("Your move> ").strip()
        except EOFError:
            print()
            break

        if user_input.lower() in {"q", "quit", "exit"}:
            break
        if not user_input:
            continue

        try:
            player_choice = parse_choice(user_input)
        except ValueError as err:
            print(err)
            continue

        result, cpu_choice = play_one_round(player_choice, rng)
        rounds_played += 1

        if result == "tie":
            ties += 1
            print(f"You chose {player_choice.value}, computer chose {cpu_choice.value}. It's a tie.")
        elif result == "player":
            player_wins += 1
            print(
                f"You chose {player_choice.value}, computer chose {cpu_choice.value}. You win this round!"
            )
        else:
            computer_wins += 1
            print(
                f"You chose {player_choice.value}, computer chose {cpu_choice.value}. Computer wins this round."
            )

        print(f"Score — You: {player_wins} | Computer: {computer_wins} | Ties: {ties}")

    print("Final score:")
    print(f"  You: {player_wins}")
    print(f"  Computer: {computer_wins}")
    print(f"  Ties: {ties}")

    if player_wins > computer_wins:
        print("Result: You win!")
        return 0
    if computer_wins > player_wins:
        print("Result: Computer wins.")
        return 0
    print("Result: It's a draw.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Rock-Paper-Scissors CLI game")
    parser.add_argument(
        "--player",
        help="Your move for a one-shot round: rock/r, paper/p, scissors/s",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible computer choices",
    )
    parser.add_argument(
        "--best-of",
        type=int,
        dest="best_of",
        help="Play a finite match interactively (odd number: 3, 5, 7).",
    )

    args = parser.parse_args()

    rng = random.Random(args.seed)

    if args.player:
        try:
            player_choice = parse_choice(args.player)
        except ValueError as err:
            print(err)
            return 2
        result, cpu_choice = play_one_round(player_choice, rng)
        if result == "tie":
            print(
                f"You: {player_choice.value} | Computer: {cpu_choice.value} | Result: tie"
            )
            return 0
        if result == "player":
            print(
                f"You: {player_choice.value} | Computer: {cpu_choice.value} | Result: you win"
            )
            return 0
        print(
            f"You: {player_choice.value} | Computer: {cpu_choice.value} | Result: computer wins"
        )
        return 0

    return interactive_loop(rng, best_of=args.best_of)


if __name__ == "__main__":
    raise SystemExit(main())