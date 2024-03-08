def rodar_esquerda(grid):
    new_grid = [[0, 0], [0, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            new_grid[len(grid[i])-1-j][i] = grid[i][j]
    return new_grid

def rodar_direita(grid):
    new_grid = [[0, 0], [0, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            new_grid[j][len(grid)-1-i] = grid[i][j]
    return new_grid

def rodar(grid, start_row, end_row, start_col, end_col, lado):
    new_grid = [grid[start_row][start_col:end_col + 1], grid[end_row][start_col:end_col + 1]]
    print(new_grid)

    
    if lado == "esquerda":
        new_grid = rodar_esquerda(new_grid)
    else:
        new_grid = rodar_direita(new_grid)
    print(new_grid)

    grid[start_row][start_col:end_col+1] = new_grid[0]
    grid[end_row][start_col:end_col+1] = new_grid[1]
    return grid



def aztec(grid, moves):

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pass

    #aux = rodar_direita(grid)
    #print("rodou:\n", aux)   
    #aux = rodar_esquerda(grid)
    #print("rodou:\n", aux)
    start_row = 0
    start_col = 0
    aux = rodar(grid, start_row, start_row + 1, start_col, start_col + 1, "direita")
    #aux = rodar(grid, 0, 1, 1, 2, "esquerda")
    print("rodou:\n", aux) 


    return 0


def main():
    T = int(input())
    for i in range(T):
        rows, columns, moves = map(int, input().split())
        G = [[0 for i in range(columns)] for j in range(rows)]

        for j in range(rows):
            G[j][:] = map(int, input().split())
        
        print(G)
        min = aztec(G, moves)	

        if min == -1:
            print("the treasure is lost!")
        else:
            print(min)









def left_rotate(self, node, child_node):
    if node is None or child_node is None:
        return None

    if child_node.left_child:
        node.right_child = child_node.left_child
        node.right_child.parent = node
    else:
        node.right_child = None

    if node.parent is not None:
        if node.parent.right_child == node:
            node.parent.right_child = child_node
        else:
            node.parent.left_child = child_node
        child_node.parent = node.parent
    else:
        child_node.parent = None
        self.root = child_node

    child_node.left_child = node
    node.parent = child_node

    node.height -= 1

def right_rotate(self, node, child_node):
    if node is None or child_node is None:
        return None

    if child_node.right_child:
        node.left_child = child_node.right_child
        node.left_child.parent = node
    else:
        node.left_child = None

    if node != self.root:
        child_node.parent = node.parent
        if node.parent.right_child == node:
            node.parent.right_child = child_node
        else:
            node.parent.left_child = child_node
    else:
        child_node.parent = None
        self.root = child_node

    child_node.right_child = node
    node.parent = child_node

    node.height -= 1





if __name__ == "__main__":
    main()