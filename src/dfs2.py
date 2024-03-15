def rodar(grid, row, col, lado):
    new_grid = [r[:] for r in grid]

    if lado == "esquerda":
        new_grid[row][col], new_grid[row][col + 1], new_grid[row + 1][col], new_grid[row + 1][col + 1] = \
        grid[row + 1][col], grid[row][col], grid[row + 1][col + 1], grid[row][col + 1]
    else:
        new_grid[row][col], new_grid[row][col + 1], new_grid[row + 1][col], new_grid[row + 1][col + 1] = \
        grid[row][col + 1], grid[row + 1][col + 1], grid[row][col], grid[row + 1][col]

    return new_grid


def is_goal_state(grid):
    for i, row in enumerate(grid):
        if any(cell != i + 1 for cell in row):
            return False
    return True

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

def solve_aztec_vault(grid, moves):
    result = dfs(grid, moves)
    return result if result is not None else "the treasure is lost!"

def main():
    T = int(input())
    for _ in range(T):
        R, C, M = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(R)]
        print(solve_aztec_vault(grid, M))

if __name__ == "__main__":
    main()