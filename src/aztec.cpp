#include <iostream>
#include <vector>
#include <deque>
#include <set>
#include <tuple>
#include <string>
#include <algorithm> // For std::max
#include <cmath> // For std::abs

using namespace std;

typedef vector<vector<int>> Grid;
typedef tuple<int, int> GridState;

// Calculate the maximum Manhattan distance in the grid
int manhattan_distance(const vector<vector<int>>& grid) {
    int total_distance = 0;
    int max_distance = 0;
    for (int row = 0; row < grid.size(); ++row) {
        for (int col = 0; col < grid[0].size(); ++col) {
            int current_value_row = (grid[row][col] - 1);
            total_distance = abs(current_value_row - row);
            max_distance = max(max_distance, total_distance);
        }
    }
    return max_distance;
}

// Check if the matrix is "almost sorted"
bool esta_praticamente_ordenada(const vector<vector<int>>& matriz) {
    for (int i = 0; i < matriz.size(); ++i) {
        int count = 0;
        for (int cell : matriz[i]) {
            if (cell != i + 1) ++count;
        }
        if (count > matriz[0].size() / 2) return false;
    }
    return true;
}

// Check if the grid is large
bool is_large_grid(int R, int C, const vector<vector<int>>& G) {
    return (R == 4 || R == 5) && (C == 4 || C == 5) && !esta_praticamente_ordenada(G);
}

// Rotate a 2x2 sub-grid within the grid
vector<vector<int>> rotate_grid(const vector<vector<int>>& grid, int row, int col, const string& direction) {
    vector<vector<int>> new_grid = grid;
    if (direction == "esquerda") {
        new_grid[row][col] = grid[row+1][col];
        new_grid[row][col+1] = grid[row][col];
        new_grid[row+1][col] = grid[row+1][col+1];
        new_grid[row+1][col+1] = grid[row][col+1];
    } else { // Assuming direction "direita"
        new_grid[row][col] = grid[row][col+1];
        new_grid[row][col+1] = grid[row+1][col+1];
        new_grid[row+1][col] = grid[row][col];
        new_grid[row+1][col+1] = grid[row+1][col];
    }
    return new_grid;
}

// Check if the grid is in a goal state
bool is_goal_state(const vector<vector<int>>& grid) {
    for (int row_index = 0; row_index < grid.size(); ++row_index) {
        for (int col_index = 0; col_index < grid[row_index].size(); ++col_index) {
            if (grid[row_index][col_index] != row_index + 1) {
                return false;
            }
        }
    }
    return true;
}

// Breadth-First Search
int bfs(const Grid& grid, const Grid& objetivo, int moves) {
    deque<pair<Grid, int>> fronteira = {{grid, 0}};
    set<Grid> visitados;
    visitados.insert(grid);

    while (!fronteira.empty()) {
        auto [estadoAtual, movimentos] = fronteira.front();
        fronteira.pop_front();
        if (estadoAtual == objetivo) {
            return movimentos;
        }
        if (movimentos >= moves) {
            continue;
        }

        for (int i = 0; i < grid.size() - 1; ++i) {
            for (int j = 0; j < grid[0].size() - 1; ++j) {
                for (const string& rotacao : {"esquerda", "direita"}) {
                    Grid novoEstado = rotate_grid(estadoAtual, i, j, rotacao);

                    if (novoEstado == objetivo) {
                        return movimentos + 1;
                    }

                    if (visitados.find(novoEstado) == visitados.end()) {
                        visitados.insert(novoEstado);
                        fronteira.push_back({novoEstado, movimentos + 1});
                    }
                }
            }
        }
    }
    return -1; // Indicating the treasure is lost or goal is unreachable within given moves
}

// Depth-First Search Helper
int dfs_helper(const Grid& grid, int moves_left, int current_depth, set<Grid>& visited) {
    if (visited.find(grid) != visited.end()) {
        return -1; // Using -1 to indicate failure
    }

    visited.insert(grid);

    if (is_goal_state(grid)) {
        return current_depth;
    }

    if (moves_left == 0) {
        return -1; // Indicating the treasure is lost
    }

    for (int row = 0; row < grid.size() - 1; ++row) {
        for (int col = 0; col < grid[0].size() - 1; ++col) {
            for (const string& direction : {"left", "right"}) {
                if (manhattan_distance(grid) > moves_left) {
                    continue; // Optimization step, can be removed
                }
                Grid new_grid = rotate_grid(grid, row, col, direction);
                int result = dfs_helper(new_grid, moves_left - 1, current_depth + 1, visited);
                if (result != -1) {
                    return result;
                }
            }
        }
    }

    return -1; // The treasure is lost
}

// Depth-First Search
int dfs(const Grid& grid, int moves_left) {
    set<Grid> visited;
    return dfs_helper(grid, moves_left, 0, visited);
}

int aztec(const Grid& grid, int moves, int rows, int columns) {
    if (manhattan_distance(grid) > moves) {
        return -1; // Indicating the treasure is lost
    }

    Grid objetivo(rows, vector<int>(columns));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < columns; ++j) {
            objetivo[i][j] = i + 1;
        }
    }
    if (is_large_grid(rows, columns, grid)) {
        return dfs(grid, moves);
    } else {
        return bfs(grid, objetivo, moves);
    }
}

int main() {
    int T;
    cin >> T;
    for (int t = 0; t < T; ++t) {
        int rows, columns, moves;
        cin >> rows >> columns >> moves;
        Grid G(rows, vector<int>(columns));
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                cin >> G[i][j];
            }
        }
        
        int result = aztec(G, moves, rows, columns);
        if (result == -1) {
            cout << "the treasure is lost!" << endl;
        } else {
            cout << result << endl;
        }
    }
    return 0;
}