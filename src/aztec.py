def rodar_esquerda(grid):
    new_grid = [[0, 0], [0, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            new_grid[len(grid[i])-1-j][i] = grid[i][j]
    return new_grid

def rodar_direita(grid):
    new_grid = [[0, 0], [0, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            new_grid[j][len(grid)-1-i] = grid[i][j]
    return new_grid

def rodar(grid, row, col, lado):
    new_grid = [grid[row][col:col + 2], grid[row + 1][col:col + 2]]
    print(new_grid)

    
    if lado == "esquerda":
        new_grid = rodar_esquerda(new_grid)
    else:
        new_grid = rodar_direita(new_grid)
    print(new_grid)

    grid[row][col:col + 2] = new_grid[0]
    grid[row + 1][col:col + 2] = new_grid[1]
    return grid



def aztec(grid, moves):

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pass

    start_row = 0
    start_col = 0
    aux = rodar(grid, start_row, start_col, "direita")
    print("rodou:\n", aux) 


    return 0


def main():
    T = int(input())
    for i in range(T):
        rows, columns, moves = map(int, input().split())
        G = [[0 for i in range(columns)] for j in range(rows)]

        for j in range(rows):
            G[j][:] = map(int, input().split())
        
        print(G)
        min = aztec(G, moves)	

        if min == -1:
            print("the treasure is lost!")
        else:
            print(min)




if __name__ == "__main__":
    main()