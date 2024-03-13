#include <iostream>
#include <vector>
#include <deque>
#include <tuple>
#include <unordered_set>

std::vector<std::vector<int>> rodar_esquerda(const std::vector<std::vector<int>>& grid) {
    return { {grid[1][0], grid[0][0]}, {grid[1][1], grid[0][1]} };
}

std::vector<std::vector<int>> rodar_direita(const std::vector<std::vector<int>>& grid) {
    return { {grid[0][1], grid[1][1]}, {grid[0][0], grid[1][0]} };
}

std::vector<std::vector<int>> rodar(const std::vector<std::vector<int>>& grid, int row, int col, const std::string& lado) {
    std::vector<int> row1(grid[row].begin() + col, grid[row].begin() + col + 2);
    std::vector<int> row2(grid[row + 1].begin() + col, grid[row + 1].begin() + col + 2);
    std::vector<std::vector<int>> new_grid = {row1, row2};

    if (lado == "esquerda") {
        new_grid = rodar_esquerda(new_grid);
    } else {
        new_grid = rodar_direita(new_grid);
    }

    std::vector<std::vector<int>> result = grid;
    result[row].erase(result[row].begin() + col, result[row].begin() + col + 2);
    result[row].insert(result[row].begin() + col, new_grid[0].begin(), new_grid[0].end());
    result[row + 1].erase(result[row + 1].begin() + col, result[row + 1].begin() + col + 2);
    result[row + 1].insert(result[row + 1].begin() + col, new_grid[1].begin(), new_grid[1].end());

    return result;
}

std::string aztec(const std::vector<std::vector<int>>& grid, int moves) {
    int rows = grid.size();
    int cols = grid[0].size();
    std::vector<std::vector<int>> objetivo(rows, std::vector<int>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            objetivo[i][j] = i * cols + j + 1;
        }
    }

    std::deque<std::pair<std::vector<std::vector<int>>, int>> fronteira;
    fronteira.emplace_back(grid, 0);

    std::unordered_set<std::string> visitados;
    std::string grid_str;
    for (const auto& row : grid) {
        for (int val : row) {
            grid_str += std::to_string(val) + ",";
        }
    }
    visitados.insert(grid_str);

    while (!fronteira.empty()) {
        auto [estadoAtual, movimentos] = fronteira.front();
        fronteira.pop_front();

        if (estadoAtual == objetivo) {
            return std::to_string(movimentos);
        }

        if (movimentos >= moves) {
            continue;
        }

        for (int i = 0; i < rows - 1; ++i) {
            for (int j = 0; j < cols - 1; ++j) {
                for (const auto& rotacao : {"esquerda", "direita"}) {
                    auto novoEstado = rodar(estadoAtual, i, j, rotacao);
                    std::string estado_str;
                    for (const auto& row : novoEstado) {
                        for (int val : row) {
                            estado_str += std::to_string(val) + ",";
                        }
                    }

                    if (novoEstado == objetivo) {
                        return std::to_string(movimentos + 1);
                    }

                    if (visitados.count(estado_str) == 0) {
                        visitados.insert(estado_str);
                        fronteira.emplace_back(novoEstado, movimentos + 1);
                    }
                }
            }
        }
    }

    return "the treasure is lost!";
}

int main() {
    int T;
    std::cin >> T;

    for (int _ = 0; _ < T; ++_) {
        int rows, columns, moves;
        std::cin >> rows >> columns >> moves;

        std::vector<std::vector<int>> G(rows, std::vector<int>(columns));
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                std::cin >> G[i][j];
            }
        }

        std::cout << aztec(G, moves) << "\n";
    }

    return 0;
}