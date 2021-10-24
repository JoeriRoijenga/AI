import random
import itertools
import math
import numpy as np
weigths = [[0.135, 0.121, 0.102, 0.0999],
            [0.0997, 0.088, 0.076, 0.0724],
            [0.0606, 0.0562, 0.0371, 0.0161],
            [0.0125, 0.0099, 0.0057, 0.0033]]

MAX_DEPTH = 3

def merge_left(b):
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b


def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}


def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False


def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue


def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'


def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)


def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys())), -1


def get_possible_moves(b):
    possible_moves = []
    for move in MERGE_FUNCTIONS.keys():
        new_b = play_move(b, move)

        if new_b != b:
            possible_moves.append(move)

    return possible_moves


def get_expectimax_move(b, depth, player):
    if depth == 0:
        return -1, eval_empty_cells(b) + eval_weights(b)

    if player is True:
        best_value = -100000
        best_move = ""

        for choice in get_possible_moves(b):
            temp_board = b.copy()
            # temp_board = play_move(temp_board, choice)

            if choice == 'left':
                temp_board = merge_left(temp_board)

            if choice == 'right':
                temp_board = merge_right(temp_board)

            if choice == 'up':
                temp_board = merge_up(temp_board)

            if choice == 'down':
                temp_board = merge_down(temp_board)

            _, value = get_expectimax_move(temp_board, depth - 1, False)

            if value > best_value:
                best_value = value
                best_move = choice

        return best_move, best_value
    else:
        best_value = 100000
        temp_b = b.copy()
        final_score = 0

        # Create a random 2 on the board
        for x in range(0, len(temp_b)):
            for y in range(0, len(temp_b)):
                if temp_b[x][y] == 0:

                    # Found an empty position, now place a two and
                    # a four to found out its score
                    temp_b[x][y] = 2
                    _, value = get_expectimax_move(temp_b, depth - 1, True)
                    current_value = value * .9

                    # now make a four on this position
                    temp_b[x][y] = 4
                    _, value = get_expectimax_move(temp_b, depth - 1, True)
                    current_value += value * 0.1

                    if current_value < best_value:
                        best_value = current_value
                        final_score = best_value

        return -1, final_score


def eval_empty_cells(b):
    board_sum = 0
    amount = 0

    for row in b:
        for value in row:
            if value != 0:
                board_sum += value
                amount += 1

    score = board_sum / amount

    return score


def eval_weights(b):
    return np.sum(np.array(b) * weigths)
