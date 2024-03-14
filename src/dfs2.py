def rotate(grid, row, col, direction):
    new_grid = [list(r) for r in grid]  # Deep copy
    if direction == "left":
        new_grid[row][col], new_grid[row][col+1], new_grid[row+1][col+1], new_grid[row+1][col] = \
            grid[row][col+1], grid[row+1][col+1], grid[row+1][col], grid[row][col]
    else:  # Right rotation
        new_grid[row][col], new_grid[row][col+1], new_grid[row+1][col+1], new_grid[row+1][col] = \
            grid[row+1][col], grid[row][col], grid[row][col+1], grid[row+1][col+1]
    return new_grid

def is_goal_state(grid):
    for i, row in enumerate(grid):
        if any(cell != i + 1 for cell in row):
            return False
    return True

def dfs(grid, moves_left, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    grid_tuple = tuple(map(tuple, grid))  # Represent the grid as a tuple for hashing
    if grid_tuple in visited:  # Avoid revisiting states
        return None
    visited.add(grid_tuple)

    if is_goal_state(grid):
        return current_depth  # Return the depth at which the goal state is found

    if moves_left == 0:
        return None  # No moves left to explore

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            for direction in ["left", "right"]:
                new_grid = rotate(grid, row, col, direction)
                result = dfs(new_grid, moves_left - 1, current_depth + 1, visited)
                if result is not None:
                    return result  # If a solution is found, propagate it upwards

    return None  # No solution found from this path

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