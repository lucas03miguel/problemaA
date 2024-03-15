from collections import deque

def praticamente_ordenada(matriz):
    total_fora_de_ordem = 0

    for i, linha in enumerate(matriz, 1):
        total_fora_de_ordem += sum(1 for j, val in enumerate(linha, start=1) if val != i)

    media = total_fora_de_ordem / len(matriz)
    return media <= len(matriz[0]) / 2

def rodar(grid, row, col, direction):
    new_grid = [list(r) for r in grid]
    if direction == "left":
        new_grid[row][col], new_grid[row+1][col], new_grid[row+1][col+1], new_grid[row][col+1] = \
            grid[row][col+1], grid[row][col], grid[row+1][col], grid[row+1][col+1]
    else:
        new_grid[row][col], new_grid[row+1][col], new_grid[row+1][col+1], new_grid[row][col+1] = \
            grid[row+1][col], grid[row+1][col+1], grid[row][col+1], grid[row][col]
    return new_grid

def is_goal_state(grid):
    for row_index, row in enumerate(grid, start=1):
        if any(cell != row_index for cell in row):
            return False
    return True

def bfs_solve_optimized(grid, max_moves):
    queue = deque([(grid, 0)])
    visited = set([tuple(map(tuple, grid))])
    
    while queue:
        current_grid, moves = queue.popleft()
        if is_goal_state(current_grid):
            return moves
        if moves < max_moves:
            for row in range(len(grid) - 1):
                for col in range(len(grid[0]) - 1):
                    for direction in ["left", "right"]:
                        new_grid = rodar(current_grid, row, col, direction)
                        grid_tuple = tuple(map(tuple, new_grid))
                        if grid_tuple not in visited:
                            visited.add(grid_tuple)
                            queue.append((new_grid, moves + 1))
    
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
        return None 

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            for direction in ["left", "right"]:
                new_grid = rodar(grid, row, col, direction)
                result = dfs(new_grid, moves_left - 1, current_depth + 1, visited)
                if result is not None:
                    return result

    return None


def main():
    T = int(input())
    for _ in range(T):
        rows, columns, moves = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(rows)]
        
        if praticamente_ordenada(grid):
            result = bfs_solve(grid, moves)
        else:
            result = dfs(grid, moves)
        print(result if result is not None else "the treasure is lost!")

if __name__ == "__main__":
    main()
