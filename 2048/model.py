import random
import itertools
import math

MAX_DEPTH = 3

weigths = [  0,  0,  1,  3,
             0,  1,  3,  5,
             1,  3,  5,  15,
             3,  5,  15, 30]


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


def get_expectimax_move(b, depth, player):
    if depth == 0:
        return -1, heuristic_corner(b) + heuristic_monotonicity(b) + heuristic_empty_cells(b)

    if player is True:
        best_value = -100000
        best_move = ""

        for choice in MERGE_FUNCTIONS.keys():
            temp_board = b.copy()
            temp_board = play_move(temp_board, choice)

            _, value = get_expectimax_move(temp_board, depth - 1, False)

            if value > best_value:
                best_value = value
                best_move = choice

        return best_move, best_value
    else:
        best_value = 100000
        temp_b = b.copy()

        _, value = get_expectimax_move(temp_b, depth - 1, True)
        final_score = min(value, best_value)

        return -1, final_score


def heuristic_corner(b):
    total_value = 0
    index = 0

    # Hold all the most valuable tiles in one corner
    for row in b:
        for item in row:
            if item != 0:
                total_value = total_value + (weigths[index] * 2)
            index += 1

    return total_value


def heuristic_empty_cells(b):
    # Try to keep as many empty cells as possible
    total_value = 0
    for x in range(4):
        for y in range(4):
            if b[x][y] == 0:
                total_value += 8

    return total_value


def heuristic_penalty(b):
    penalty = 0

    # Try to cluster the highest together
    for x in range(4):
        for y in range(4):
            for neighbour in get_neighbours(b, x, y):
                penalty = penalty + (b[x][y] - neighbour)

    return penalty


def heuristic_monotonicity(b):
    total_value = 0

    for x in range(4):
        for y in range(4):
            for neighbour in get_neighbours(b, x, y):
                if neighbour == b[x][y]:
                    total_value += 15

                if neighbour == b[x][y] / 2:
                    total_value += 10

                if neighbour == b[x][y] / 4:
                    total_value += 5

    return total_value


def get_neighbours(matrix, rowNumber, colNumber):
    result = []
    for rowAdd in range(-1, 2):
        newRow = rowNumber + rowAdd
        if newRow >= 0 and newRow <= len(matrix)-1:
            for colAdd in range(-1, 2):
                newCol = colNumber + colAdd
                if newCol >= 0 and newCol <= len(matrix)-1:
                    if newCol == colNumber and newRow == rowNumber:
                        continue
                    result.append(matrix[newCol][newRow])
    return result
