import threading
import random
import sys

class GameState:
    '''
    Class to save the current state of the game

    n       = number of players
    rolls   = array storing the rolled numbers
    '''
    def __init__(self, n):
        self.n = n
        self.rolls = [0]*n

class Player:
    '''
    Class to save all the needed data for each player

    not_eliminated = is this player still in the game?
    id             = id number for each player (0 - n-1)
    barrier        = barrier for syncronization
    game_state     = current state of the game, stored in the GameState class
    )'''
    def __init__(self, id, barrier, game_state):
        self.not_eliminated = True
        self.id = id
        self.barrier = barrier
        self.game_state = game_state

def player_function(player):
    '''
    player function to handle game state
    player with id 0 handles the elimination
    
    while loop iterates as long as there n > 1
    uses barriers to syncronize game state
    '''
    initial_amount_players = player.game_state.n

    while player.game_state.n > 1:
        # player is eliminated
        if not player.not_eliminated:
            player.barrier.wait()
        # player was eliminated in last round
        #  not_eliminated gets updated
        elif player.game_state.rolls[player.id] == 10:
            player.not_eliminated = False
            player.barrier.wait()
        
        # generating random number for each player
        else:
            random_number = random.randint(1,6)
            print(f"Player {player.id}: rolled a {random_number}")
            player.game_state.rolls[player.id] = random_number
            player.barrier.wait()

        player.barrier.wait()

        if player.id == 0:
            # Only consider players who are not eliminated
            active_players = [roll for roll in player.game_state.rolls if roll != 10]
            min_value = min(active_players)

            # Check if all active players rolled the same value
            same_value = len(set(active_players)) == 1

            if same_value:
                print("Repeating round\n-----------------\n")
            else:
                for i in range(initial_amount_players):
                    if player.game_state.rolls[i] == min_value:
                        print(f"Eliminating player {i}")
                        player.game_state.rolls[i] = 10
                        player.game_state.n -= 1
                print("-----------------\n")

        player.barrier.wait()

    # find the winning player
    if player.id == 0:
        for i in range(initial_amount_players):
            if player.game_state.rolls[i] != 10:
                print(f"Player {i} won the game!\n")
                break

def main():
    '''
    main function converts arguments
    initializes game
    spawns n threads 
    '''
    if len(sys.argv) != 2:
        print("incorrect usage! Usage %s <number of players", sys.argv[1])
        raise Exception("incorrect usage.")
        
    n = int(sys.argv[1])
    if n <= 0:
        raise ValueError("Invalid number of players")

    game = GameState(n)
    barrier = threading.Barrier(n)
    threads = []
    players = []

    # create new player with the given attributes and threads
    for i in range(n):
        player = Player(i, barrier, game)
        thread = threading.Thread(target=player_function, args=(player,))
        threads.append(thread)
        players.append(player)
        thread.start()

    for thread in threads:
        thread.join()

    print("Game over!")

if __name__ == "__main__":
    main() 
