import numpy as np
import os

def generate_random_block(m, n):
    matrix = np.zeros((m, n), dtype=int)
    for i in range(m):
        for j in range(n):
            matrix[i][j] = np.random.randint(0, 2)
    return matrix

def dfs(matrix, i, j):
    if i < 0 or i >= len(matrix) or j < 0 or j >= len(matrix[0]) or matrix[i][j] != 1:
        return
    matrix[i][j] = -1
    dfs(matrix, i + 1, j)
    dfs(matrix, i - 1, j)
    dfs(matrix, i, j + 1)
    dfs(matrix, i, j - 1)

def count_connected_regions(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                dfs(matrix, i, j)
                count += 1
    return count

def generate_random_warehouse(m=5, n=5, max_iter=200000):
    shape_set = []
    for _ in range(max_iter):
        block = generate_random_block(m, n)
        valid = True
        for i in range(m):
            for j in range(n):
                if block[i, j] == 1:
                    if i == 0 and j == 0 and block[1, 0] + block[0, 1] != 2:
                        valid = False
                    elif i == 0 and j == n-1 and block[1, n-1] + block[0, n-2] != 2:
                        valid = False
                    elif i == m-1 and j == 0 and block[m-2, 0] + block[m-1, 1] != 2:
                        valid = False
                    elif i == m-1 and j == n-1 and block[m-2, n-1] + block[m-1, n-2] != 2:
                        valid = False
                    elif i == 0 and 0 < j < n-1 and (block[0, j-1] + block[0, j+1] + block[1, j] < 2 or block[1, j] == 0):
                        valid = False
                    elif i == m-1 and 0 < j < n-1 and (block[m-1, j-1] + block[m-1, j+1] + block[m-2, j] < 2 or block[m-2, j] == 0):
                        valid = False
                    elif j == 0 and 0 < i < m-1 and (block[i-1, 0] + block[i+1, 0] + block[i, 1] < 2 or block[i, 1] == 0):
                        valid = False
                    elif j == n-1 and 0 < i < m-1 and (block[i-1, n-1] + block[i+1, n-1] + block[i, n-2] < 2 or block[i, n-2] == 0):
                        valid = False
                    elif 0 < i < m-1 and 0 < j < n-1 and (block[i-1, j] + block[i+1, j] + block[i, j-1] + block[i, j+1] < 2 or block[i, j-1] + block[i, j+1] == 0 or block[i-1, j] + block[i+1, j] == 0):
                        valid = False
        if valid:
            c = count_connected_regions(block.copy())
            if c == 1:
                print(block)
                if block.tolist() not in shape_set:
                    shape_set.append(block.tolist())
    return shape_set



if __name__ == "__main__":
    # (optional) Generate a random warehouse shape
    # shape_set = generate_random_warehouse(m=5, n=5, max_iter=200000)

    m, n = 2, 2
    # m, n = 3, 3
    shape_set = [np.ones((m, n), dtype=int)]

    assets_root_path = f"{os.getcwd()}/assets"
    np.save(f"{assets_root_path}/{m}x{n}_warehouse_shapes.npy", np.array(shape_set))
    print(shape_set)
