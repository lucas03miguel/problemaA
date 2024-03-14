def rotate(grid, row, col, direction):
    """Rotate a 2x2 grid within the larger grid in the specified direction."""
    new_grid = [list(row) for row in grid]  # Make a deep copy to avoid mutating the original grid
    if direction == "left":
        new_grid[row][col], new_grid[row+1][col], new_grid[row+1][col+1], new_grid[row][col+1] = \
            grid[row][col+1], grid[row][col], grid[row+1][col], grid[row+1][col+1]
    else:  # direction == "right"
        new_grid[row][col], new_grid[row+1][col], new_grid[row+1][col+1], new_grid[row][col+1] = \
            grid[row+1][col], grid[row+1][col+1], grid[row][col+1], grid[row][col]
    return new_grid

def is_goal_state(grid):
    """Check if the grid is in the goal state."""
    for i, row in enumerate(grid):
        if any(cell != i + 1 for cell in row):
            return False
    return True

def dfs(grid, moves, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    if is_goal_state(grid):
        return current_depth
    if current_depth == moves:
        return None

    grid_key = tuple(map(tuple, grid))
    if grid_key in visited:
        return None
    visited.add(grid_key)

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            for direction in ["left", "right"]:
                new_grid = rotate(grid, row, col, direction)
                result = dfs(new_grid, moves, current_depth + 1, visited)
                if result is not None:
                    return result

    return None

def solve_aztec_vault(grid, moves):
    result = dfs(grid, moves)
    return result if result is not None else "the treasure is lost!"

def main():
    T = int(input().strip())
    for _ in range(T):
        rows, columns, moves = map(int, input().strip().split())
        grid = [list(map(int, input().strip().split())) for _ in range(rows)]
        solution = solve_aztec_vault(grid, moves)
        print(solution if solution != None else "the treasure is lost!")

if __name__ == "__main__":
    main()