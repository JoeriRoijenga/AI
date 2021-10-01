# http://dhconnelly.com/paip-python/docs/paip/othello.html#strategies
# https://blog.theofekfoundation.org/artificial-intelligence/2015/12/18/minimax-improvements/
import random
import time

"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', 'X', 'O', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score
    board = initial_board()
    player = BLACK
    strategy = lambda who: black_strategy if who == BLACK else white_strategy
    while player is not None:
        move = get_move(strategy(player), player, board)
        make_move(move, player, board)
        player = next_player(board, player)
    return board, score(board)

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    copy = list(board) # copy the board to prevent cheating
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move


def score(board):
    # compute player's score (number of player's pieces minus opponent's)
    black, white = 0, 0
    opp = opponent(BLACK)
    for sq in squares():
        piece = board[sq]
        if piece == BLACK: black += 1
        elif piece == opp: white += 1
    return [black, white]

def scoreStrat(player, board):
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player: mine += 1
        elif piece == opp: theirs += 1
    return mine - theirs

# Play strategies
def random_strategy(player, board):
    return random.choice(legal_moves(player, board))

# Minimax
def minimax(player, board, depth, evaluate):
    def value(board):
        return -minimax(opponent(player), board, depth-1, evaluate)[0]

    if depth == 0:
        return evaluate(player, board), None

    moves = legal_moves(player, board)
    
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None

        return value(board), None

    return max((value(make_move(m, player, list(board))), m) for m in moves)

# Function to start minimax
def minimax_searcher(depth, evaluate):
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy


# Pruning with alphabeta
def alphabeta(player, board, alpha, beta, depth, evaluate):
    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]
    
    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None
    
    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            alpha = val
            best_move = move
    
    return alpha, best_move

# Function to call alphabeta (pruning)
def alphabeta_searcher(depth, evaluate):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]

    return strategy

# Check for which value is best choice
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
    diff = scoreStrat(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

# Start of game
if __name__ == "__main__":
    start_time = time.time()
    board, scores = play(alphabeta_searcher(6, final_value), random_strategy) # depth of 6 is +- 3 seconds
    # board, scores = play(minimax_searcher(3, final_value), random_strategy) # depth of 3 stays below 2 seconds
    end_time = time.time()
    
    print(print_board(board))
    print("black: " + str(scores[0]))
    print("white: " + str(scores[1]))

    print("runtime: " + str(end_time - start_time))