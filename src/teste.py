from collections import deque

def manhattan_distance(grid):
    total_distance = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            target_value = row + 1  # O valor que deveria estar nesta linha
            current_value_row = (grid[row][col] - 1)  # A linha onde o valor atual deveria estar
            total_distance += abs(current_value_row - row)
    return total_distance

def rotate_grid(grid, row, col, direction):
    sub_grid = [grid[row][col:col + 2], grid[row + 1][col:col + 2]]
    if direction == "esquerda":
        new_sub_grid = [[sub_grid[1][0], sub_grid[0][0]], [sub_grid[1][1], sub_grid[0][1]]]
    else:  # Corrigido para direita conforme a lógica de rotação correta
        new_sub_grid = [[sub_grid[0][1], sub_grid[1][1]], [sub_grid[0][0], sub_grid[1][0]]]
    new_grid = grid[:row] + \
               [grid[row][:col] + new_sub_grid[0] + grid[row][col+2:]] + \
               [grid[row+1][:col] + new_sub_grid[1] + grid[row+1][col+2:]] + \
               grid[row+2:]
    return new_grid

def is_large_grid(R, C):
    return R == 4 and C == 5 or R == 5 and (C == 4 or C == 5)

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
                new_grid = rotate_grid(grid, row, col, direction)
                result = dfs(new_grid, moves_left - 1, current_depth + 1, visited)
                if result is not None:
                    return result

    return "the treasure is lost!"

def aztec(grid, moves):
    # Pré-processamento: Verifica se a distância de Manhattan mínima excede o número de movimentos disponíveis
    if manhattan_distance(grid) > moves:
        return "the treasure is lost!"
    
    objetivo = [[(i + 1) for _ in range(len(grid[0]))] for i in range(len(grid))]
    if is_large_grid(len(grid), len(grid[0])):
        return dfs(grid, moves)
    else:
        return bfs(grid, objetivo, moves)


def main():
    T = int(input(""))
    for _ in range(T):
        rows, columns, moves = map(int, input().split())
        G = [list(map(int, input().split())) for _ in range(rows)]
        
        min_value = aztec(G, moves)    
        print(min_value)

if __name__ == "__main__":
    main()
