
# Multi-Threaded Dice Game

This repository contains Python Code for a multi-threaded dice game. 

## Overview

The game involves a number of players (simulated by a thread) rolling a dice, with the player rolling the smallest number being eliminated in each round. If all players roll the same number, the round is repeated. The last remaining player is declared the winner. The whole game mechanics are managed in the thread function.

The script makes use of Python's threading module to simulate each player as a separate thread. The `threading.Barrier` class is used to synchronize the threads, ensuring that each round of the game (i.e., each set of dice rolls) is completed before any player is eliminated.

## Usage

The script takes a single command line argument which is the number of players. 

For example, to start a game with 5 players, run:

```
python3.10 dice_game.py 5
```

## Code Structure

- The `GameState` class stores the current state of the game, including the number of remaining players and an array of the most recent roll of each player.

- The `Player` class represents each player in the game. It keeps track of whether the player has been eliminated, the player's ID, a reference to the game state, and a barrier used for synchronization.

- The `player_function` function is the function executed by each player thread. It handles the logic of the game, including dice rolls, checking for round repetition, and player elimination.

- The `main` function parses the command line argument, initializes the game state and player threads, and starts the threads.

