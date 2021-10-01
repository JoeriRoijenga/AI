import itertools

floors = [0, 1, 2, 3, 4]

def check_floors(L, M, N, E, J):
    return (L != 4) and (M != 0) and ((N != 0 and N != 4) and (N - 1 != M and N + 1 != M)) and (E > M) and (J - 1 != N and J + 1 != N)
    
if __name__ == "__main__":        
    currentHouse = {}

    for (L, M, N, E, J) in list(itertools.permutations(floors)):
        if check_floors(L, M, N, E, J):           
            currentHouse[L] = "L"
            currentHouse[M] = "M"
            currentHouse[N] = "N"
            currentHouse[E] = "E"
            currentHouse[J] = "J"
            break
    
    print(currentHouse)

