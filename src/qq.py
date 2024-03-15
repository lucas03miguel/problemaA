from collections import deque

def rodar_esquerda(grid):
    return [[grid[1][0], grid[0][0]], [grid[1][1], grid[0][1]]]

def rodar_direita(grid):
    return [[grid[0][1], grid[1][1]], [grid[0][0], grid[1][0]]]

def rodar(grid, row, col, lado):
    new_grid = [grid[row][col:col + 2], grid[row + 1][col:col + 2]]

    if lado == "esquerda":
        new_grid = rodar_esquerda(new_grid)
    else:
        new_grid = rodar_direita(new_grid)
    
    return grid[:row] + [grid[row][:col] + new_grid[0] + grid[row][col+2:]] + \
           [grid[row+1][:col] + new_grid[1] + grid[row+1][col+2:]] + grid[row+2:]

def bfs(grid, objetivo, moves):
    visitados = set()
    fila = deque([(grid, 0)])  # Cada elemento é uma tupla (configuração do grid, número de movimentos)
    visitados.add(tuple(map(tuple, grid)))
    
    while fila:
        estadoAtual, movimentos = fila.popleft()
        if estadoAtual == objetivo:
            return movimentos
        if movimentos < moves:
            for i in range(len(grid) - 1):
                for j in range(len(grid[0]) - 1):
                    for lado in ["esquerda", "direita"]:
                        novoEstado = rodar(estadoAtual, i, j, lado)
                        estadoTupla = tuple(map(tuple, novoEstado))
                        if estadoTupla not in visitados:
                            visitados.add(estadoTupla)
                            fila.append((novoEstado, movimentos + 1))
    
    return "the treasure is lost!"

def aztec(grid, moves):
    objetivo = [[i + 1 for _ in range(len(grid[0]))] for i in range(len(grid))]
    resultado = bfs(grid, objetivo, moves)
    return resultado


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