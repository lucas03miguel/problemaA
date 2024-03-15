#include <iostream>
#include <vector>
#include <algorithm>

std::vector<std::vector<int>> rodarEsquerda(const std::vector<std::vector<int>>& grid) {
    return {{grid[1][0], grid[0][0]}, {grid[1][1], grid[0][1]}};
}

std::vector<std::vector<int>> rodarDireita(const std::vector<std::vector<int>>& grid) {
    return {{grid[0][1], grid[1][1]}, {grid[0][0], grid[1][0]}};
}

std::vector<std::vector<int>> rodar(const std::vector<std::vector<int>>& grid, int row, int col, const std::string& lado) {
    std::vector<std::vector<int>> new_grid = {
        std::vector<int>(grid[row].begin() + col, grid[row].begin() + col + 2),
        std::vector<int>(grid[row + 1].begin() + col, grid[row + 1].begin() + col + 2)
    };

    if (lado == "esquerda") {
        new_grid = rodarEsquerda(new_grid);
    } else {
        new_grid = rodarDireita(new_grid);
        }

        std::vector<std::vector<int>> result = grid;
        result[row].erase(result[row].begin() + col, result[row].begin() + col + 2);
        result[row].insert(result[row].begin() + col, new_grid[0].begin(), new_grid[0].end());

        result[row + 1].erase(result[row + 1].begin() + col, result[row + 1].begin() + col + 2);
        result[row + 1].insert(result[row + 1].begin() + col, new_grid[1].begin(), new_grid[1].end());

        return result;
        }

int aztec(const std::vector<std::vector<int>>& grid, int moves) {
    int rows = grid.size(), cols = grid[0].size();
    std::vector<std::vector<int>> objetivo(rows, std::vector<int>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            objetivo[i][j] = i + 1;
        }
    }

    std::vector<std::vector<std::vector<int>>> visitados(rows, std::vector<std::vector<int>>(cols, std::vector<int>(cols, 0)));
    std::vector<std::vector<std::vector<int>>> fronteira;
    fronteira.push_back(grid);
    std::vector<int> movimentos_fronteira(1, 0);

    while (!fronteira.empty()) {
        std::vector<std::vector<std::vector<int>>> next_fronteira;
        std::vector<int> next_movimentos_fronteira;

        for (int i = 0; i < (int)fronteira.size(); ++i) {
            const auto& estadoAtual = fronteira[i];
            int movimentos = movimentos_fronteira[i];

            if (estadoAtual == objetivo) {
                return movimentos;
            }
            if (movimentos >= moves) {
                continue;
            }

            for (int row = 0; row < rows - 1; ++row) {
                for (int col = 0; col < cols - 1; ++col) {
                    for (auto rotacao : {"esquerda", "direita"}) {
                        auto novoEstado = rodar(estadoAtual, row, col, rotacao);
                        if (novoEstado == objetivo) {
                            return movimentos + 1;
                        }
                        if (visitados[row][col][col] == 0) {
                            visitados[row][col][col] = 1;
                            next_fronteira.push_back(novoEstado);
                            next_movimentos_fronteira.push_back(movimentos + 1);
                        }
                    }
                }
            }
        }

        fronteira = std::move(next_fronteira);
        movimentos_fronteira = std::move(next_movimentos_fronteira);
    }

    return -1; // "the treasure is lost!"
}

int main() {
    int T;
    std::cin >> T;

    for (int _ = 0; _ < T; ++_) {
        int rows, columns, moves;
        std::cin >> rows >> columns >> moves;

        std::vector<std::vector<int>> grid(rows, std::vector<int>(columns));
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                std::cin >> grid[i][j];
            }
        }

        int min_value = aztec(grid, moves);
        std::cout << min_value << std::endl;
    }

    return 0;
}