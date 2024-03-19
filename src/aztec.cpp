#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

vector<vector<int>> rodarEsquerda(const vector<vector<int>>& grid) {
    return {{grid[1][0], grid[0][0]}, {grid[1][1], grid[0][1]}};
}

vector<vector<int>> rodarDireita(const vector<vector<int>>& grid) {
    return {{grid[0][1], grid[1][1]}, {grid[0][0], grid[1][0]}};
}

vector<vector<int>> rodar(const vector<vector<int>>& grid, int row, int col, const string& lado) {
    vector<vector<int>> new_grid = {
        vector<int>(grid[row].begin() + col, grid[row].begin() + col + 2),
        vector<int>(grid[row + 1].begin() + col, grid[row + 1].begin() + col + 2)
    };

    if (lado == "esquerda") {
        new_grid = rodarEsquerda(new_grid);
    } else {
        new_grid = rodarDireita(new_grid);
        }

        vector<vector<int>> result = grid;
        result[row].erase(result[row].begin() + col, result[row].begin() + col + 2);
        result[row].insert(result[row].begin() + col, new_grid[0].begin(), new_grid[0].end());

        result[row + 1].erase(result[row + 1].begin() + col, result[row + 1].begin() + col + 2);
        result[row + 1].insert(result[row + 1].begin() + col, new_grid[1].begin(), new_grid[1].end());

        return result;
        }

int aztec(const vector<vector<int>>& grid, int moves) {
    int rows = grid.size(), cols = grid[0].size();
    vector<vector<int>> objetivo(rows, vector<int>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            objetivo[i][j] = i + 1;
        }
    }

    vector<vector<vector<int>>> visitados(rows, vector<vector<int>>(cols, vector<int>(cols, 0)));
    vector<vector<vector<int>>> fronteira;
    fronteira.push_back(grid);
    vector<int> movimentos_fronteira(1, 0);

    while (!fronteira.empty()) {
        vector<vector<vector<int>>> next_fronteira;
        vector<int> next_movimentos_fronteira;

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

        fronteira = move(next_fronteira);
        movimentos_fronteira = move(next_movimentos_fronteira);
    }

    return -1; // "the treasure is lost!"
}

int main() {
    int T;
    cin >> T;

    for (int _ = 0; _ < T; ++_) {
        int rows, columns, moves;
        cin >> rows >> columns >> moves;

        vector<vector<int>> grid(rows, vector<int>(columns));
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                cin >> grid[i][j];
            }
        }

        int min_value = aztec(grid, moves);
        cout << min_value << endl;
    }

    return 0;
}