import time

left = ["F", "G", "C", "W"]
right = []

rules = {
    "G":["C", "W"],
    "W":["G"],
    "C":["G"],
}

def printStates():
    print('States:')
    print('left: ', left)
    print('right: ', right)
    print()

if __name__ == "__main__":    
    run = True
    while run:
        printStates()
        right.insert(0, left.pop(0))

        for rule in rules[left[0]]:
            if rule in right: 
                left.append(right.pop(right.index(rule)))
                break

        right.append(left.pop(0))
        
        if len(left) > 0:
            printStates()
            left.insert(0, right.pop(0))
        else:
            run = False
        time.sleep(1)
    print('Done')
    printStates()

