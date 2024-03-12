#include <iostream>
#include <vector>
#include <deque>
#include <set>
#include <tuple>

using namespace std;

vector<vector<int>> rodar_esquerda(const vector<vector<int>>& grid) {
    return {{grid[1][0], grid[0][0]}, {grid[1][1], grid[0][1]}};
}

vector<vector<int>> rodar_direita(const vector<vector<int>>& grid) {
    return {{grid[0][1], grid[1][1]}, {grid[0][0], grid[1][0]}};
}

vector<vector<int>> rodar(const vector<vector<int>>& grid, int row, int col, const string& lado) {
    vector<vector<int>> new_grid = {{grid[row][col], grid[row][col + 1]},
                                    {grid[row + 1][col], grid[row + 1][col + 1]}};

    if (lado == "esquerda") {
        new_grid = rodar_esquerda(new_grid);
    } else {
        new_grid = rodar_direita(new_grid);
    }

    vector<vector<int>> result = grid;
    result[row][col] = new_grid[0][0];
    result[row][col + 1] = new_grid[0][1];
    result[row + 1][col] = new_grid[1][0];
    result[row + 1][col + 1] = new_grid[1][1];
    
    return result;
}


string aztec(vector<vector<int>>& grid, int moves) {
    vector<vector<int>> objetivo(grid.size(), vector<int>(grid[0].size()));
    for (size_t i = 0; i < objetivo.size(); ++i) {
        for (size_t j = 0; j < objetivo[i].size(); ++j) {
            objetivo[i][j] = i + 1;
        }
    }

    deque<pair<vector<vector<int>>, int>> fronteira;
    fronteira.push_back(make_pair(grid, 0));
    set<vector<vector<int>>> visitados;
    visitados.insert(grid);

    while (!fronteira.empty()) {
        auto [estadoAtual, movimentos] = fronteira.front();
        fronteira.pop_front();
        
        if (estadoAtual == objetivo) {
            return to_string(movimentos);
        }
        if (movimentos >= moves) {
            continue;
        }

        for (int i = 0; i < static_cast<int>(grid.size()) - 1; ++i) {
            for (int j = 0; j < static_cast<int>(grid[0].size()) - 1; ++j) {
                for (auto rotacao : {"esquerda", "direita"}) {
                    auto novoEstado = rodar(estadoAtual, i, j, rotacao);
                    
                    if (novoEstado == objetivo) {
                        return to_string(movimentos + 1);
                    }

                    if (visitados.find(novoEstado) == visitados.end()) {
                        visitados.insert(novoEstado);
                        fronteira.push_back(make_pair(novoEstado, movimentos + 1));
                    }
                }
            }
        }
    }
    return "the treasure is lost!";
}

int main() {
    int T;
    cin >> T;
    for (int _ = 0; _ < T; ++_) {
        int rows, columns, moves;
        cin >> rows >> columns >> moves;
        vector<vector<int>> G(rows, vector<int>(columns));

        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                cin >> G[i][j];
            }
        }
        
        cout << aztec(G, moves) << endl;
    }

    return 0;
}
