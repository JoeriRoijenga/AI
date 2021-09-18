import random
from time import sleep

state_left = "FCWG"
state_right = ""
# A list that contains the moves from left to right and then right to left
invalid_moves = {}  # {("CW", "G"): true, ("WG", "C"): False}


def move_right(passenger, has_passenger):
    global state_left, state_right

    # Get the right character from the left string and move it to the right string
    if has_passenger:
        for char in state_left:
            if char == passenger:
                # Remove the character and the 'farmer'
                state_left = state_left.replace(passenger, "")
                state_left = state_left.replace("F", "")

                # Add the character
                state_right += "F"
                state_right += passenger
                print_screen()
    else:
        state_left = state_left.replace("F", "")
        state_right += "F"
        print_screen()


def move_left(passenger, has_passenger):
    global state_left, state_right

    # Get the right character from the left string and move it to the right string
    if has_passenger:
        for char in state_right:
            if char == passenger:
                # Remove the character and the 'farmer'
                state_right = state_right.replace(passenger, "")
                state_right = state_right.replace("F", "")

                # Add the character
                state_left += "F"
                state_left += passenger
                print_screen()
    else:
        state_right = state_right.replace("F", "")
        state_left += "F"
        print_screen()


def check_valid_state(state):
    # Function that checks if a pair of things is allowed

    # When a farmer is present, any combination is valid
    if "F" in state:
        return True

    # The goat will eat the coal
    if "C" in state and "G" in state:
        return False

    # The wolf will eat the goat
    if "G" in state and "W" in state:
        return False

    # Anything else
    return True


def print_screen():
    # Print the states of both sides of the river to the CLI
    print(state_left + "||" + state_right)
    print("----------------")


def start():
    # Start the algorithm

    # Show the start state
    print_screen()

    global state_left, state_right

    last_left, last_right = "", ""

    while True:
        if "F" in state_right and "C" in state_right and "W" in state_right and "G" in state_right:
            break
        # sleep(3)
        # When the farmer is on the left side, move someone to the right
        if "F" in state_left:
            # Select a random passenger
            passenger = state_left.replace("F", "")[random.randint(0, len(state_left.replace("F", "")) - 1)]

            # Before we move, save the current setting
            # if the move is not allowed, we backtrack to this setting

            last_left, last_right = state_left, state_right

            # Decide whether the farmer has to move alone or he should take a passenger with him
            if state_left == "FG" or state_left == "GF":
                move_right("G", True)

            if len(state_left) == 2 and len(state_right) == 2:
                move_right(None, False)
            else:
                move_right(passenger, True)

            if check_valid_state(state_left) and check_valid_state(state_right):
                continue
            else:
                # this move is not allowed, save it in the cache and backtrack to the previous setting
                state_left, state_right = last_left, last_right
                print("Backtracking...")

            print_screen()

        else:
            # Select a random passenger
            passenger = state_right.replace("F", "")[random.randint(0, len(state_right.replace("F", "")) - 1)]

            # Before we move, save the current setting
            # if the move is not allowed, we backtrack to this setting

            last_left, last_right = state_left, state_right
            # Decide whether the farmer has to move alone or he should take a passenger with him
            if len(state_right) == 3 and check_valid_state(state_right.replace("F", "")):
                move_left(None, False)
            else:
                if len(state_left) == 2 and len(state_right) == 2:
                    move_left(None, False)
                else:
                    move_left(passenger, True)

            if check_valid_state(state_left) and check_valid_state(state_right):
                continue
            else:
                # this move is not allowed, save it in the cache and backtrack to the previous setting
                state_left, state_right = last_left, last_right
                print("Backtracking...")

            print_screen()

    print("Done!")


start()
