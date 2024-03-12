from collections import deque
from copy import deepcopy

def rodar_esquerda(grid):
    return [[grid[1][0], grid[0][0]], [grid[1][1], grid[0][1]]]

def rodar_direita(grid):
    return [[grid[0][1], grid[1][1]], [grid[0][0], grid[1][0]]]


def rodar(grid, row, col, lado):
    new_grid = [grid[row][col:col + 2], grid[row + 1][col:col + 2]]
    new_grid = rodar_esquerda(new_grid) if lado == "esquerda" else rodar_direita(new_grid)
    return grid[:row] + [grid[row][:col] + new_grid[0] + grid[row][col+2:]] + \
           [grid[row+1][:col] + new_grid[1] + grid[row+1][col+2:]] + grid[row+2:]

def aztec(grid, moves):
    objetivo = [[(i + 1) for _ in range(len(grid[0]))] for i in range(len(grid))]
    fronteira = deque([(grid, 0)])
    visitados = set()
    visitados.add(tuple(map(tuple, grid)))

    while fronteira:
        estadoAtual, movimentos = fronteira.popleft()
        if estadoAtual == objetivo:
            return movimentos
        if movimentos >= moves:
            continue

        for i in range(len(grid) - 1):
            for j in range(len(grid[0]) - 1):
                for rotacao in ["esquerda", "direita"]:
                    novoEstado = rodar(estadoAtual, i, j, rotacao)
                    estadoTupla = tuple(map(tuple, novoEstado))
                    if estadoTupla not in visitados:
                        visitados.add(estadoTupla)
                        fronteira.append((novoEstado, movimentos + 1))
                        if novoEstado == objetivo:
                            return movimentos + 1
                        
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