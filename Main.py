import random
from Path import is_valid_move, dfs, find_all_paths

class wall:
    def __init__(self, orient, x, y):
        self.orient = orient
        self.x = x
        self.y = y

class square_data:
    def __init__(self, config, wall_left, wall_right, wall_up, wall_down):
        self.config = config
        self.walls = [wall_left, wall_right, wall_up, wall_down]

# Possible wall configurations of a square
# sintax = [wall_left, wall_right, wall_up, wall_down] / 0 - No wall / 1 - wall
Configs = {"1": [1,0,0,0],
           "2": [0,0,1,0],
           "3": [0,1,0,0],
           "4": [0,0,0,1],
           "5": [1,0,0,1],
           "6": [0,1,0,1],
           "7": [0,1,1,0],
           "8": [1,0,1,0],
           "9": [1,1,0,0],
           "10": [0,0,1,1],
           "11": [1,1,0,1],
           "12": [0,1,1,1],
           "13": [1,1,1,0],
           "14": [0,1,1,1],
           "15": [0,0,0,0],
           "16": [1,1,1,1]}

def generate_random_except_15():
    while True:
        random_number = random.randint(1, 16)
        if random_number != 15:
            return random_number

# Center of the maze coordenates
Center_of_maze = [ (7,7), (7,8), (8,7), (8,8)]

def print_maze( num_nodes, adjacency_matrix_vert, adjacency_matrix_hori):
    for i in range(num_nodes):
        for j in range(num_nodes):
            if j < 16:
                print("*", end="")
                if adjacency_matrix_hori[i][j] == 1:
                    print(" -- ", end="")
                else:
                    print("    ", end="")
            else:
                print("*")
        if i < 16:
            for x in range(num_nodes):
                if adjacency_matrix_vert[i][x] == 1:
                    print("|", end="")
                else:
                    print(" ", end="")
                if x < 16:
                    print("    ", end="")
                else:
                    print("")

def update_matrix_of_maze( i, j, Squares, adjacency_matrix_vert, adjacency_matrix_hori):
    data = Squares[i][j]
    is_Wall = Configs[str(data.config)]
    for x in range(4):
            data_wall = data.walls[x]
            if data_wall.orient == "vert":
                adjacency_matrix_vert[data_wall.x][data_wall.y] = is_Wall[x]
            else:
                adjacency_matrix_hori[data_wall.x][data_wall.y] = is_Wall[x]

def paths():
    matrix_16x16 = [[0] * 16 for _ in range(16)]
    start_row, start_col = 15, 0
    end_row, end_col = 7, 7
    path_limit = 100
    paths = find_all_paths(matrix_16x16, start_row, start_col, end_row, end_col, path_limit)
    return paths

def special_cases(x,y,Possible_set):
    #Left walls
    if 1<=x<=14 and y==0:
        set = {1,5,8,9,11,13,14,16}
    #Right walls
    elif 1 <= x <= 14 and y == 15:
        set = {3,6,7,9,11,12,13,16}
    #Top walls
    elif 1 <= y <= 14 and x == 0:
        set = {2,7,8,10,12,13,14,16}
    #Bottom walls
    elif 1 <= y <= 14 and x == 15:
        set = {4,5,6,10,11,12,14,16}
    #Corners
    elif x == 0 and y == 0:
        set = {8,13,14,16}
    elif x == 15 and y == 0:
        set = {5, 11, 14}
    elif x == 0 and y == 15:
        set = {7,12,13,16}
    elif x == 15 and y == 15:
        set = {6,11,12,16}
    else:
        set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16}
    Possible_set = Possible_set & set
    return Possible_set

# Vector of the squares
n_squares_per_line = 16
Squares = [[0 for _ in range(n_squares_per_line)] for _ in range(n_squares_per_line)]

# Create a 17x17 adjacency matrix for an undirected graph
num_nodes = 17
adjacency_matrix_hori = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
adjacency_matrix_vert = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

# Fill the vector with the data and create the maze
for i in range(n_squares_per_line):
    for j in range(n_squares_per_line):
        config = generate_random_except_15()
        wall_left = wall( "vert", i, j)
        wall_right = wall( "vert", i, j+1)
        wall_up = wall( "hori", i, j)
        wall_down = wall( "hori", i+1, j)
        Squares[i][j] = square_data( config, wall_left, wall_right, wall_up, wall_down)
        # define the configs of the squares
        update_matrix_of_maze(i, j, Squares, adjacency_matrix_vert, adjacency_matrix_hori)


Squares[7][7].config = "8"
update_matrix_of_maze(7, 7, Squares, adjacency_matrix_vert, adjacency_matrix_hori)
Squares[8][7].config = "5"
update_matrix_of_maze(8, 7, Squares, adjacency_matrix_vert, adjacency_matrix_hori)
Squares[7][8].config = "7"
update_matrix_of_maze(7, 8, Squares, adjacency_matrix_vert, adjacency_matrix_hori)
Squares[8][8].config = "6"
update_matrix_of_maze(8, 8, Squares, adjacency_matrix_vert, adjacency_matrix_hori)

paths = paths()

print(paths[1])

for x in range(len(paths[1])):
    # X is the destiny
    if x-1>=0:
        (d1,d2) = paths[1][x]
        (d3,d4) = paths[1][x - 1]
        delta1 = (d1-d3,d2-d4)
        # bottom
        if delta1 == (-1, 0):
            set1 = {1, 2, 3, 7, 8, 9, 13}
        # top
        elif delta1 == (1, 0):
            set1 = {1, 3, 4, 5, 6, 9, 11}
        # right
        elif delta1 == (0, 1):
            set1 = {1, 2, 4, 5, 8, 10, 14}
        # left
        elif delta1 == (0, -1):
            set1 = {2, 3, 4, 6, 7, 10, 12}
    else:
        set1 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16}


    # x is the departure
    if x+1<len(paths[1]):
        (d1, d2) = paths[1][x+1]
        (d3, d4) = paths[1][x]
        delta2 = (d1 - d3, d2 - d4)
        # top
        if delta2 == (-1, 0):
            set2 = {1, 3, 4, 5, 6, 9, 11}
        # bottom
        elif delta2 == (1, 0):
            set2 = {1, 2, 3, 7, 8, 9, 13}
        # left
        elif delta2 == (0, 1):
            set2 = {1, 2, 4, 5, 8, 10, 14}
        # right
        elif delta2 == (0, -1):
            set2 = {2, 3, 4, 6, 7, 10, 12}
    else:
        set2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16}

    Possible_set = set1 & set2
    a1 = paths[1][x][0]
    a2 = paths[1][x][1]
    print(str(x) + ": (" + str(a1) + "," + str(a2) + ")  " + str(Possible_set))
    set = special_cases(a1,a2,Possible_set)
    print(str(x) + ": (" + str(a1) + "," + str(a2) + ")  " + str(set))
    x_config = random.choice(list(set))
    Squares[a1][a2].config = str(x_config)
    update_matrix_of_maze(a1, a2, Squares, adjacency_matrix_vert, adjacency_matrix_hori)
    print(str(x) + ": (" + str(a1) + "," + str(a2) + ")  " + str(x_config))

print_maze(num_nodes,adjacency_matrix_vert,adjacency_matrix_hori)




with open('.txt', 'w') as file:
    file.write('Feel free to customize the content.\n')

print('Text file generated successfully: output.txt')