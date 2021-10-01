import itertools

floors = [0, 1, 2, 3, 4]
person = ["L", "M", "N", "E", "J"]

def check_floors(L, M, N, E, J):
    return (L != 4) and (M != 0) and ((N != 0 and N != 4) and (N - 1 != M and N + 1 != M)) and (E > M) and (J - 1 != N and J + 1 != N)
    
if __name__ == "__main__":        
    currentHouse = {}

    for (L, M, N, E, J) in list(itertools.permutations(floors)):
        if check_floors(L, M, N, E, J):
            for index, floor in enumerate([L, M, N, E, J]):
                currentHouse[floor] = person[index]
            break
    
    print(currentHouse)

