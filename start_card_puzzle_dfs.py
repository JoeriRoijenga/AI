import itertools
'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbours = {0: [3], 1: [2], 2: [1, 4, 3], 3: [0, 2, 5], 4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}


def is_valid(board):
    for key, value in board.items():
        for neighbour in neighbours[key]:
            if ace_king_neighbour(value, board[neighbour]) and queen_ace_neighbour(value, board[neighbour]) and queen_king_neighbour(value, board[neighbour]) and queen_farmer_neighbour(value, board[neighbour]) and same_neighbours(value, board[neighbour]):
                continue
            else:
                return False

    return True


def ace_king_neighbour(one, two):
    if one == 'K' and two == 'A' or one == 'A' and two == 'K':
        return True

    if one == '.' or two == '.':
        return True

    return True


def queen_king_neighbour(one, two):
    if one == 'K' and two == 'Q' or one == 'Q' and two == 'K':
        return True

    return True


def queen_farmer_neighbour(one, two):
    if one == 'Q' and two == 'J' or one == 'J' and two == 'Q':
        return True

    return True


def queen_ace_neighbour(one, two):
    if one == 'Q' and two == 'A' or one == 'A' and two == 'Q':
        return False

    return True


def same_neighbours(one, two):
    if one == '.':
        return True

    if two == '.':
        return True

    if one == two:
        return False
    else:
        return True


def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ', is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ', is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3]
    print('f ', is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ', is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ', is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))


def brute_force():
    # Create all possible options
    valid_options = []
    options = (list(itertools.permutations(cards)))

    # Put them on the board check if its a valid combination
    for option in options:
        board = {cell: '.' for cell in range(8)}
        for key, value in board.items():
            board[key] = option[key]

        if is_valid(board):
            valid_options.append(board)

    return valid_options


def solve(board):
    print(board)
    index = 0
    if is_valid(board):

        # Check if there are any options left
        found = False
        for key, value in board.items():
            if value == '.':
                index = key
                found = True

        # When there everything is filled
        if found is False:
            print(board)
            return True

        # Try all possible solutions
        for card in cards:
            # Place the card at the next possible position
            cards.remove(card)
            board[index] = card
            if solve(board):
                return True

            cards.append(card)
            board[index] = '.'

    return False


# print(brute_force())
solve(start_board)
