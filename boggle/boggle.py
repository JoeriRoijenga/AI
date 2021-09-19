board = [
    ["h", "u", "i", "s"],
    ["s", "q", "r", "f"],
    ["w", "c", "a", "t"],
    ["u", "w", "g", "x"]
]

possible_words = ["huis", "rat"]


def get_neighbours(x, y):
    global board

    output = []

    if x + 1 > len(board) - 1:
        output.append((0, y))
    else:
        output.append((x + 1, y))

    if x - 1 < 0:
        output.append((len(board) - 1, y))
    else:
        output.append((x - 1, y))

    if y + 1 > len(board) - 1:
        output.append((x, 0))
    else:
        output.append((x, y + 1))

    if y - 1 < 0:
        output.append((x, len(board) - 1))
    else:
        output.append((x, y - 1))

    return output


def search(x, y, current_word, index):
    global possible_words, board

    if current_word in possible_words:
        print("Found", current_word)

    for word in possible_words:
        for location in get_neighbours(x, y):

            next_char = board[location[0]][location[1]]
            try:
                if word[index + 1] == next_char:
                    search(location[0], location[1], current_word + next_char, index + 1)
            except IndexError:
                return False

    # If this statement is reached there are no possible words
    return False


def start():
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            search(x, y, board[x][y], 0)


if __name__ == '__main__':
    start()
