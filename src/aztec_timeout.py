from collections import deque
from threading import Thread
import time

class AztecFunctionThread(Thread):
    def __init__(self, grid, moves, rows, columns):
        Thread.__init__(self)
        self.grid = grid
        self.moves = moves
        self.rows = rows
        self.columns = columns
        self.result = None

    def run(self):
        self.result = aztec(self.grid, self.moves, self.rows, self.columns)


def distance_row(grid):
    total_distance = 0
    max_distance = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            current_value_row = (grid[row][col] - 1)
            total_distance = abs(current_value_row - row)
            if total_distance > max_distance:
                max_distance = total_distance

    return max_distance

def distance_column(grid):
    total_distance = 0
    max_distance = 0
    
    fora_lugar = {i: 0 for i in range(1, len(grid) + 1)}
    for i, row in enumerate(grid, start=1):
        for j, cell in enumerate(row):
            #print("cell", cell, i, j)
            if cell != i:
                fora_lugar[i] = j
    #print(fora_lugar)

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            current_value = (grid[row][col] - 1)
            total_distance = abs(current_value - fora_lugar[current_value + 1])
            if total_distance > max_distance:
                max_distance = total_distance
    return max_distance

def praticamente_ordenada(matriz):
    total_fora_de_ordem = 0
    n_linhas = len(matriz)
    n_colunas = len(matriz[0])

    for i, linha in enumerate(matriz):
        for valor in linha:
            if valor != i + 1:
                total_fora_de_ordem += 1
        if total_fora_de_ordem > n_colunas / 2:
            return False

    if total_fora_de_ordem / n_linhas > n_colunas / 2:
        return False
    return True

def is_large_grid(R, C, G):
    return ((R in {4, 5}) and (C in {4, 5})) and not praticamente_ordenada(G)

def rotate_grid(grid, row, col, direction):
    sub_grid = [grid[row][col:col + 2], grid[row + 1][col:col + 2]]
    if direction == "esquerda":
        new_sub_grid = [[sub_grid[1][0], sub_grid[0][0]], [sub_grid[1][1], sub_grid[0][1]]]
    else:
        new_sub_grid = [[sub_grid[0][1], sub_grid[1][1]], [sub_grid[0][0], sub_grid[1][0]]]
    new_grid = grid[:row] + \
               [grid[row][:col] + new_sub_grid[0] + grid[row][col+2:]] + \
               [grid[row+1][:col] + new_sub_grid[1] + grid[row+1][col+2:]] + \
               grid[row+2:]
    return new_grid

def is_goal_state(grid):
    for row_index, row in enumerate(grid, start=1):
        if any(cell != row_index for cell in row):
            return False
    return True

def bfs(grid, objetivo, moves):
    fronteira = deque([(grid, 0)])
    visitados = set()
    visitados.add(tuple(map(tuple, grid)))

    while fronteira:
        estadoAtual, movimentos = fronteira.popleft()
        if estadoAtual == objetivo:
            return movimentos
        if movimentos >= moves:
            continue

        #print("moves:", movimentos, moves)
        for i in range(len(grid) - 1):
            for j in range(len(grid[0]) - 1):
                for rotacao in ["esquerda", "direita"]:
                    #if distance_row(estadoAtual) + movimentos > moves:
                    #    continue

                    novoEstado = rotate_grid(estadoAtual, i, j, rotacao)
                    estadoTupla = tuple(map(tuple, novoEstado))
                    #print(novoEstado)

                    if novoEstado == objetivo:
                        return movimentos + 1
                    
                    if estadoTupla not in visitados:
                        visitados.add(estadoTupla)
                        fronteira.append((novoEstado, movimentos + 1))

    return "the treasure is lost!"

def dfs(grid, moves_left, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    if is_goal_state(grid):
        return current_depth 

    if moves_left == 0:
        return "the treasure is lost!" 

    grid_tuple = tuple(map(tuple, grid)) 
    if grid_tuple in visited:
        return None
    
    visited.add(grid_tuple)

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            for direction in ["left", "right"]:
                if distance_row(grid) > moves_left or distance_column(grid) > moves_left:
                    continue
                
                new_grid = rotate_grid(grid, row, col, direction)
                result = dfs(new_grid, moves_left - 1, current_depth + 1, visited)
                if result is not None:
                    return result

    return "the treasure is lost!"

def aztec(grid, moves, rows, columns):
    count = {i: 0 for i in range(1, rows + 1)}
    for row in grid:
        for cell in row:
            count[cell] += 1
    if any(value != columns for value in count.values()):
        return "the treasure is lost!"
    
    if distance_row(grid) > moves or distance_column(grid) > moves:
        return "the treasure is lost!"
    
    #print(distance_column(grid))
    
    objetivo = [[(i + 1) for _ in range(len(grid[0]))] for i in range(len(grid))]
    if is_large_grid(rows, columns, grid):
        return dfs(grid, moves)
    else:
        return bfs(grid, objetivo, moves)


def main():
    print("", file=open("tests/matrizes_timeout.txt", "w"))
    T = int(input())
    for _ in range(T):
        rows, columns, moves = map(int, input().split())
        G = [list(map(int, input().split())) for _ in range(rows)]
        
        aztec_thread = AztecFunctionThread(G, moves, rows, columns)
        aztec_thread.start()
        aztec_thread.join(timeout=1)  # Espera por 1 segundo

        if aztec_thread.is_alive():
            print("---------TIMEOUT---------\n")
            print(rows, columns, moves, file=open("tests/matrizes_timeout.txt", "a"))
            for row in G:
                print(" ".join(map(str, row)), file=open("tests/matrizes_timeout.txt", "a"))
            print("", file=open("tests/matrizes_timeout.txt", "a"))
            print("-------------------------")
            aztec_thread.join()
        result = aztec(G, moves, rows, columns)
        print(result)

if __name__ == "__main__":
    main()