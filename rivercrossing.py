# Used example: https://stackoverflow.com/questions/64974829/search-not-working-for-river-crossing-problem-in-python
import copy

# Character positions
F = 0
G = 1
C = 2
W = 3

# Starting state
START = ["L", "L", "L", "L"]

# Moment when all characters are on the right side
def is_goal(node):
    return node == ["R", "R", "R", "R"]

# Rules
def checkRuleWolf(node):
    return node[F] == node[W] or node[W] != node[G] 

def checkRuleGoat(node):
    return node[F] == node[G] or node[G] != node[C] 

def checkRules(node):
    return checkRuleGoat(node) and checkRuleWolf(node)

def checkMoves(moves):
    return [ move for move in moves if checkRules(move)]

# Get next nodes
def successors(node):
    for character in [F, G, C, W]:
        if node[F] == node[character]:
            move = copy.copy(node)
            move[F] = 'L' if node[F] == 'R' else 'R'
            move[character] = 'L' if node[character] == 'R' else 'R'
            yield move # More memory efficient, handles per move instead of returning a whole list at once

# Depth First Search
def find_all_paths(node, path = []):
    path += [node]

    if is_goal(node):
        return [path]
    
    paths = [] # a list of paths
    
    for child in checkMoves(successors(node)):
        # If not in current path
        if child not in path:
            # return list of paths from here
            newpaths = find_all_paths(child, path)

            # add every path found to paths
            for newpath in newpaths:
                paths.append(newpath)
            
            # After finding the correct path, it add faulthy data
            if len(paths) > 0:
                break;

    return paths



# Start program
if __name__ == "__main__":    
    assert(checkRuleWolf(["L", "L", "L", "L"]) == True)
    assert(checkRuleWolf(["R", "L", "R", "L"]) == False)
    assert(checkRuleWolf(["R", "L", "L", "R"]) == True)
    
    assert(checkRules(["L", "L", "L", "L"]) == True)

    assert(list(successors(START)) == [['R','L','L','L'],['R','R','L','L'],['R','L','R','L'],['R','L','L','R']])
    assert(list(checkMoves(successors(START))) == [['R','R','L','L']])

    # Print every single step
    for path in find_all_paths(START)[0]:
        print(path)