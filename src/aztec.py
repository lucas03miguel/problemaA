from collections import deque
from copy import deepcopy

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
    grid_copia = deepcopy(grid)
    new_grid = [grid_copia[row][col:col + 2], grid_copia[row + 1][col:col + 2]]
    #print(new_grid)

    if lado == "esquerda":
        new_grid = rodar_esquerda(new_grid)
    else:
        new_grid = rodar_direita(new_grid)
    #print(new_grid)

    grid_copia[row][col:col + 2] = new_grid[0]
    grid_copia[row + 1][col:col + 2] = new_grid[1]

    # Retorna a cópia atualizada
    return grid_copia



def aztec(grid, moves):
    objetivo = [(len(grid[0])) * [(i + 1)] for i in range(len(grid))]
    
    fronteira = deque()
    fronteira.append((grid, 0))
    visitados = []
    visitados.append(grid)

    while fronteira:
        estadoAtual, movimentos = fronteira.popleft()
        
        if estadoAtual == objetivo:
            return movimentos
        
        if movimentos >= moves:
            continue 
        
        for i in range(len(grid) - 1):
            for j in range(len(grid[i]) - 1):
                for rotacao in ["esquerda", "direita"]:
                    novoEstado = rodar(estadoAtual, i, j, rotacao)

                    if novoEstado == objetivo:
                        return movimentos + 1
                    
                    if novoEstado not in visitados:
                        visitados.append(novoEstado)
                        fronteira.append((novoEstado, movimentos + 1))

    return "the treasure is lost!"


def main():
    T = int(input())
    for _ in range(T):
        rows, columns, moves = map(int, input().split())
        G = []

        for j in range(rows):
            row = map(int, input().split())
            G.append(list(row))
        
        min = aztec(G, moves)	
        print(min)


if __name__ == "__main__":
    main()