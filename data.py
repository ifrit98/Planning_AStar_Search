from PIL import Image
from math import inf
import os

WHITE = 'white.txt'
BROWN = 'brown.txt'
RED = 'red.txt'
IMG = 'terrain.png'
ELEVATION = "mpp.txt"
MOVE_COST = {1:10.29,
        2:10.29,
        3:7.55,
        4:7.55}
PATH_COLORS = {'red.txt':(255,0,0,255), # Red
               'brown.txt':(162,0,255,  255), # Violet
               'white.txt':(128,0,128,255)} # Purple
TERRAIN = {      (248,148,18,255):1, # Open land
                 (255,192,0,255):7, # Rough meadow
                 (255,255,255,255):3, # Easy movement forest
                 (2,208,60,255):4, # Slow run forest
                 (2,136,40,255):5, # Walk forest
                 (71,51,3,255):1, # Paved road
                 (0,0,0,255):1, # Footpath
                 (135,206,235,255):4, # Ice
                 (139, 69, 19, 255):5, # Mud
                 (205,0,101,255):inf, # Out of bounds
                 (0,0,255,255):inf, # Lake/Swamp/Marsh
                 (5,73,24,255):inf} # Impassible vegetation

def process_data(map, grph):
    elevation_map = get_elevation(ELEVATION)
    matrix, full_graph = convert_to_node(grph, map, elevation_map)
    add_neighbors(matrix)
    return full_graph, matrix

def load_img(img):
    im = Image.open(img)
    return im

def create_course_pngs(courses, season):
    for course in courses:
        im = Image.open(season + '.png')
        im.save(season + ' - ' + course[:-3] + 'png')

def get_elevation(elev):
    elevation_matrix = [[0 for i in range(500)] for j in range(395)]
    i, j = 0,0
    with open(elev) as file:
        for line in file:
            toks = line.strip().split()
            toks = toks[:-5]
            for tok in toks:
                elevation_matrix[j][i] = float(tok)
                j += 1
            i += 1
            j = 0
    return elevation_matrix

def read_goals(fn):
    goals = []
    f = open(fn)
    for line in f:
        str = line.strip().split()
        goals.append([int(str[0]),int(str[1])])
    return goals

def convert_to_node(graph, terrain_matrix, elev_matrix):
    node_matrix = [[0 for i in range(499)] for j in range(394)]
    for i in range(0, 394):
        for j in range(0, 499):
            terrain = TERRAIN[terrain_matrix[i,j]]
            node_matrix[i][j] = graph.addVertex((i,j), terrain, elev_matrix[i][j])
    return node_matrix, graph

def get_neighbors(pointXY, grid):
    x, y = pointXY
    neighbors = []
    if x - 1 >= 0:
        neighbors.append(grid[x-1][y]) # West
    if x + 1 <= 393:
        neighbors.append(grid[x+1][y]) # East
    if y - 1 >= 0:
        neighbors.append(grid[x][y-1]) # South
    if y + 1 <= 498:
        neighbors.append(grid[x][y+1]) # North
    return neighbors

def add_neighbors(node_matrix):
    for i in range(0, 394):
        for j in range(0, 499):
            node = node_matrix[i][j]
            childID = 1
            for nbr in get_neighbors(node.point, node_matrix):
                node.addNeighbor(nbr, childID)
                childID += 1

def mark_path(path, clr, season):
    color = PATH_COLORS[clr]
    im = load_img(season + ' - ' + clr[:-4] + '.png')
    map = im.load()
    for i in range(len(path)):
        node = path[i]
        x,y = node.point
        map[x, y] = color
    im.save(season + ' - ' + clr[:-4] + '.png')

def cleanup():
    print('Done!')
    print('Cleaning up... removing extra files')
    os.remove('winter.png')
    os.remove('spring.png')
    os.remove('summer.png')
    os.remove('fall.png')