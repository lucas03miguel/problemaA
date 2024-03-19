from collections import deque

def manhattan_distance(grid):
    total_distance = 0
    max_distance = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            current_value_row = (grid[row][col] - 1)
            total_distance = abs(current_value_row - row)
            if total_distance > max_distance:
                max_distance = total_distance

    return max_distance

def esta_praticamente_ordenada(matriz):
    contagem = []
    for i in range(len(matriz)):
        contagem_fora_de_ordem = 0
        for j in range(len(matriz[0])):
            if matriz[i][j] != i + 1:
                contagem_fora_de_ordem += 1
        contagem.append(contagem_fora_de_ordem)

    media = sum(contagem) / len(contagem)
    if media > len(matriz[0]) / 2:
        return False
    return True

def is_large_grid(R, C, G):
    return (((R == 4 or R == 5) and (C == 4 or C == 5))) and not esta_praticamente_ordenada(G)

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

        for i in range(len(grid) - 1):
            for j in range(len(grid[0]) - 1):
                for rotacao in ["esquerda", "direita"]:
                    novoEstado = rotate_grid(estadoAtual, i, j, rotacao)
                    estadoTupla = tuple(map(tuple, novoEstado))

                    if novoEstado == objetivo:
                        return movimentos + 1
                    
                    if estadoTupla not in visitados:
                        visitados.add(estadoTupla)
                        fronteira.append((novoEstado, movimentos + 1))
    return "the treasure is lost!"

def dfs(grid, moves_left, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    grid_tuple = tuple(map(tuple, grid)) 
    if grid_tuple in visited:
        return None
    
    visited.add(grid_tuple)

    if is_goal_state(grid):
        return current_depth 
    
    if moves_left == 0:
        return "the treasure is lost!" 

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            for direction in ["left", "right"]:
                if manhattan_distance(grid) > moves_left:
                    return "the treasure is lost!"
                new_grid = rotate_grid(grid, row, col, direction)
                result = dfs(new_grid, moves_left - 1, current_depth + 1, visited)
                if result is not None:
                    return result

    return "the treasure is lost!"

def aztec(grid, moves, rows, columns):
    if manhattan_distance(grid) > moves:
        return "the treasure is lost!"
    
    objetivo = [[(i + 1) for _ in range(len(grid[0]))] for i in range(len(grid))]
    if is_large_grid(rows, columns, grid):
        return dfs(grid, moves)
    else:
        return bfs(grid, objetivo, moves)


def main():
    T = int(input(""))
    for _ in range(T):
        rows, columns, moves = map(int, input().split())
        G = [list(map(int, input().split())) for _ in range(rows)]
        
        min_value = aztec(G, moves, rows, columns)    
        print(min_value)

if __name__ == "__main__":
    main()