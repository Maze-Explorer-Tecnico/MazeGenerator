def is_valid_move(matrix, visited, row, col):
    # Check if the move is within the matrix bounds and not visited
    return 0 <= row < len(matrix) and 0 <= col < len(matrix[0]) and not visited[row][col]

def dfs(matrix, visited, path, row, col, end_row, end_col, all_paths, path_limit):
    if row == end_row and col == end_col:
        # Destination reached, add the path to the list
        all_paths.append(path.copy())
        return

    visited[row][col] = True

    # Explore all possible moves: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for move in moves:
        new_row, new_col = row + move[0], col + move[1]
        if is_valid_move(matrix, visited, new_row, new_col):
            dfs(matrix, visited, path + [(new_row, new_col)], new_row, new_col, end_row, end_col,all_paths, path_limit)

            # Stop the search if the path limit is reached
            if len(all_paths) >= path_limit:
                return

    visited[row][col] = False

def find_all_paths(matrix, start_row, start_col, end_row, end_col,path_limit):
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    path = [(start_row, start_col)]
    all_paths = []
    dfs(matrix, visited, path, start_row, start_col, end_row, end_col, all_paths, path_limit)
    return all_paths
