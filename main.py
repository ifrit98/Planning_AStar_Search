from data import *
from graph import Graph
from A_Star import a_star_search, reconstruct_path
from seasons import update_fall_terrain, process_map

def main():
    seasons = ['winter', 'spring', 'summer', 'fall']
    courses = [WHITE, RED, BROWN]
    for season in seasons:
        print('Processing', season, 'map...')
        if season == 'fall':
            update_fall_terrain()
            im, map = process_map(IMG, season)
        elif season == 'spring':
            im, map = process_map(IMG, season, 15)
        elif season == 'winter':
            im, map = process_map(IMG, season, 7)
        else:
            im, map = process_map(IMG, season)
        print('Writing new course png files to be used...')
        create_course_pngs(courses, season)
        print('Building graph...')
        print()
        grph = Graph()
        full_graph, matrix = process_data(map, grph)

        for course in courses:
            path_len, path_len_m, i = 0, 0, 0
            goals = read_goals(course)
            print('Starting', course[:-4], 'course in', season, 'season...')
            while i < len(goals)-1:
                start = matrix[goals[i][0]][goals[i][1]]
                end = matrix[goals[i+1][0]][goals[i+1][1]]
                came_from, total_cost, path_in_meters = a_star_search(full_graph, start, end)
                path = reconstruct_path(came_from, start, end)
                path_len += len(path)
                path_len_m += path_in_meters
                mark_path(path, course, season)
                i += 1
            print('Path length for', course[:-4], 'course in', season, 'season is:', path_len, 'nodes')
            print('Path length in meters:', path_len_m)
            print()

    cleanup()

if __name__ == "__main__":
    main()