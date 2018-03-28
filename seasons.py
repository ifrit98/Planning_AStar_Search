from PIL import Image
from que import Queue
from data import get_elevation, TERRAIN

ELEVATION = get_elevation('mpp.txt')
IMG = 'terrain - Copy.png'
ICE = (135,206,235,255)
MUD = (139,69,19,255)
WATER = (0,0,255,255)
OUTOFBOUNDS = (205,0,101,255)

def get_neighbors(pointXY, depth=1, add_diag=True):
    x, y = pointXY
    neighbors = []
    if x - depth >= 0:
        neighbors.append((x-depth, y)) # West
    if x + depth <= 393:
        neighbors.append((x+depth, y)) # East
    if y - depth >= 0:
        neighbors.append((x, y-depth)) # South
    if y + depth <= 498:
        neighbors.append((x, y+depth)) # North
    if add_diag:
        if x - depth >= 0 and y - depth >= 0:
            neighbors.append((x-depth, y-depth)) # SouthWest
        if x - depth >= 0 and y + depth <= 498:
            neighbors.append((x-depth, y+depth)) # NorthWest
        if x + depth >= 0 and y - depth <= 498:
            neighbors.append((x+depth, y-depth)) # SouthEast
        if x + depth >= 0 and y + depth <= 498:
            neighbors.append((x+depth, y+depth)) # NorthEast
    return neighbors

def do_season_change(map, start, max_depth, season):
    x,y = start
    pix_coord = []
    spring_condition = map[x,y] == WATER
    winter_condition = map[x,y] != WATER
    if (season == 'spring' and winter_condition) or (season == 'winter' and spring_condition):
        return []
    queue = Queue()
    queue.enqueue(start)
    visited = set()
    depth = 0
    next_to_incr = 0
    elem_to_incr = 1

    while not queue.isEmpty():
        current = queue.dequeue()
        visited.add(current)
        neighbors = set(get_neighbors(current)).difference(visited)
        visited = visited.union(neighbors)
        for neighbor in neighbors:
            m,n = neighbor
            if map[m,n] == OUTOFBOUNDS:
                continue
            if (season == 'spring' and map[m,n] != WATER) or \
               (season == 'winter' and map[m,n] == WATER):
                queue.enqueue(neighbor)
                next_to_incr += 1
                if season == 'winter' or ELEVATION[m][n] - ELEVATION[x][y] > 1:
                    pix_coord.append(neighbor)
        elem_to_incr -= 1
        if elem_to_incr == 0:
            depth += 1
            elem_to_incr = next_to_incr
            next_to_incr = 0
        if depth >= max_depth:
            break

    return pix_coord

def process_map(map, season, depth=0):
    im = Image.open(map)
    loaded_map = im.load()
    if season == 'summer' or season =='fall':
        im.save(season + '.png')
        return im, loaded_map
    if season == 'winter':
        color = ICE
    else:
        color = MUD
    pixels = []
    for i in range(0,394):
        for j in range(0,499):
            if loaded_map[i,j] == OUTOFBOUNDS:
                continue
            coord = (i,j)
            output_coord = do_season_change(loaded_map, coord, depth, season)
            if output_coord:
                pixels.extend(output_coord)
    fill(loaded_map, pixels, color, season)
    im.save(season + '.png')
    return im, loaded_map

def fill(map, pixel_list, color, season):
    print('List of pixels to change for', season,':')
    print(pixel_list)
    print()
    for pixel in pixel_list:
        x,y = pixel
        map[x, y] = color
    return map

def update_fall_terrain(increase=4):
    TERRAIN[(255, 255, 255, 255)] += increase
    TERRAIN[(2, 208, 60, 255)] += increase
    TERRAIN[(2, 136, 40, 255)] += increase