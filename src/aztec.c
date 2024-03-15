#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROWS 4
#define MAX_COLS 4
#define MAX_STATES 10000

typedef struct {
    int grid[MAX_ROWS][MAX_COLS];
    int rows;
    int cols;
} Grid;

typedef struct Node {
    Grid grid;
    int moves;
    struct Node* next;
} Node;

typedef struct {
    Node* front;
    Node* rear;
} Queue;

void initQueue(Queue* q) {
    q->front = q->rear = NULL;
}

int isEmpty(Queue* q) {
    return q->front == NULL;
}

void enqueue(Queue* q, Grid grid, int moves) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->grid = grid;
    newNode->moves = moves;
    newNode->next = NULL;

    if (isEmpty(q)) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

void dequeue(Queue* q, Grid* grid, int* moves) {
    if (isEmpty(q)) {
        return;
    }

    Node* temp = q->front;
    *grid = q->front->grid;
    *moves = q->front->moves;
    q->front = q->front->next;

    if (q->front == NULL) {
        q->rear = NULL;
    }

    free(temp);
}

int isGoalState(Grid* grid) {
    for (int i = 0; i < grid->rows; ++i) {
        for (int j = 0; j < grid->cols; ++j) {
            if (grid->grid[i][j] != i * grid->cols + j + 1) {
                return 0;
            }
        }
    }
    return 1;
}

void rotate(Grid* grid, int row, int col, int direction, Grid* newGrid) {
    *newGrid = *grid; // Copy grid
    if (direction == 0) { // Rotate left
        int temp = newGrid->grid[row][col];
        newGrid->grid[row][col] = newGrid->grid[row][col+1];
        newGrid->grid[row][col+1] = newGrid->grid[row+1][col+1];
        newGrid->grid[row+1][col+1] = newGrid->grid[row+1][col];
        newGrid->grid[row+1][col] = temp;
    } else { // Rotate right
        int temp = newGrid->grid[row+1][col+1];
        newGrid->grid[row+1][col+1] = newGrid->grid[row][col+1];
        newGrid->grid[row][col+1] = newGrid->grid[row][col];
        newGrid->grid[row][col] = newGrid->grid[row+1][col];
        newGrid->grid[row+1][col] = temp;
    }
}

int bfs(Grid startGrid, int maxMoves) {
    Queue q;
    initQueue(&q);
    enqueue(&q, startGrid, 0);

    while (!isEmpty(&q)) {
        Grid currentGrid;
        int moves;
        dequeue(&q, &currentGrid, &moves);

        if (isGoalState(&currentGrid)) {
            return moves;
        }

        if (moves < maxMoves) {
            for (int row = 0; row < currentGrid.rows - 1; ++row) {
                for (int col = 0; col < currentGrid.cols - 1; ++col) {
                    for (int direction = 0; direction < 2; ++direction) {
                        Grid newGrid;
                        rotate(&currentGrid, row, col, direction, &newGrid);
                        enqueue(&q, newGrid, moves + 1);
                    }
                }
            }
        }
    }

    return -1; // Indica que o objetivo não foi alcançado dentro do número máximo de movimentos
}

int main() {
    int T, R, C, M;
    scanf("%d", &T);
    for (int t = 0; t < T; ++t) {
        scanf("%d %d %d", &R, &C, &M);
        Grid grid;
        grid.rows = R;
        grid.cols = C;
        for (int i = 0; i < R; ++i) {
            for (int j = 0; j < C; ++j) {
                scanf("%d", &grid.grid[i][j]);
            }
        }
        int result = bfs(grid, M);
        if (result != -1) {
            printf("%d\n", result);
        } else {
            printf("the treasure is lost!\n");
        }
    }
    return 0;
}