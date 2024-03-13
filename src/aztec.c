#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_R 5
#define MAX_C 5

typedef struct {
    int grid[MAX_R][MAX_C];
    int R, C;
} Grid;

typedef struct Node {
    Grid grid;
    int moves;
    struct Node* next;
} Node;

Node* newNode(Grid grid, int moves) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->grid = grid;
    node->moves = moves;
    node->next = NULL;
    return node;
}

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
    Node* temp = newNode(grid, moves);
    if (q->rear == NULL) {
        q->front = q->rear = temp;
        return;
    }
    q->rear->next = temp;
    q->rear = temp;
}

void dequeue(Queue* q) {
    if (isEmpty(q))
        return;
    Node* temp = q->front;
    q->front = q->front->next;
    if (q->front == NULL)
        q->rear = NULL;
    free(temp);
}

Node* front(Queue* q) {
    if (isEmpty(q))
        return NULL;
    return q->front;
}

void rotateBlock(Grid* grid, int row, int col, char direction) {
    int temp;
    if (direction == 'r') { // Rotate right
        temp = grid->grid[row][col];
        grid->grid[row][col] = grid->grid[row+1][col];
        grid->grid[row+1][col] = grid->grid[row+1][col+1];
        grid->grid[row+1][col+1] = grid->grid[row][col+1];
        grid->grid[row][col+1] = temp;
    } else if (direction == 'l') { // Rotate left
        temp = grid->grid[row][col];
        grid->grid[row][col] = grid->grid[row][col+1];
        grid->grid[row][col+1] = grid->grid[row+1][col+1];
        grid->grid[row+1][col+1] = grid->grid[row+1][col];
        grid->grid[row+1][col] = temp;
    }
}

int isTarget(Grid* grid) {
    for (int i = 0; i < grid->R; ++i)
        for (int j = 0; j < grid->C; ++j)
            if (grid->grid[i][j] != (i % grid->R) + 1)
                return 0;
    return 1;
}

int solve(Grid grid, int R, int C, int M) {
    Queue q;
    initQueue(&q);
    enqueue(&q, grid, 0);

    while (!isEmpty(&q)) {
        Node* curr = front(&q);
        Grid currGrid = curr->grid;
        int moves = curr->moves;
        dequeue(&q);

        if (isTarget(&currGrid))
            return moves;

        if (moves >= M)
            continue;

        for (int i = 0; i < R-1; ++i) {
            for (int j = 0; j < C-1; ++j) {
                Grid newGrid = currGrid;
                rotateBlock(&newGrid, i, j, 'r');
                enqueue(&q, newGrid, moves + 1);

                newGrid = currGrid;
                rotateBlock(&newGrid, i, j, 'l');
                enqueue(&q, newGrid, moves + 1);
            }
        }
    }

    return -1; // Signifies the treasure is lost
}

int main() {
    int T, R, C, M;
    scanf("%d", &T);
    for (int t = 0; t < T; ++t) {
        scanf("%d %d %d", &R, &C, &M);
        Grid grid;
        grid.R = R;
        grid.C = C;
        for (int i = 0; i < R; ++i) {
            for (int j = 0; j < C; ++j) {
                scanf("%d", &grid.grid[i][j]);
            }
        }
        int result = solve(grid, R, C, M);
        if (result != -1) {
            printf("%d\n", result);
        } else {
            printf("the treasure is lost!\n");
        }
    }
    return 0;
}