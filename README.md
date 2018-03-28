# Planning_AStar_Search

Generate optimal paths for a series of orienteering courses for all four seasons, utilizing A* search using a slightly more complex heuristic function on a 400x500 pixel terrain map with heuristic values associated with the terrain, as well as elevation and manhattan distance metric.

Input: 
- A series of courses (pixel locations) that increase in difficulty.
- 400x500 pixel terrain map

Output:
- Path costs and distances for each course in each season to stdout
- png map files of all different seasons with paths drawn
