# Planning_AStar_Search

Generate optimal paths for a series of orienteering courses for all four seasons, utilizing A* search using a slightly more complex heuristic function on a 400x500 pixel terrain map with heuristic values associated with the terrain, as well as elevation and manhattan distance metric.

Input: 
- A series of courses (pixel locations) that increase in difficulty.
- 400x500 pixel terrain map

Output:
- Path costs and distances for each course in each season to stdout
- png map files of all different seasons with paths drawn

data.py: Gathers all required data from txt files and processes it according to needs of the surrounding
programs, such as building the graph, getting neighbors, and marking the path.
seasons.py: Modifies maps for spring and winter seasons.

A_Star.py: Uses a tradition graph object that is built from nodes that are updated with terrain data that
is converted into integers from pixels, elevation data taken from mpp.txt, and a dictionary of neighbors
with weights attached corresponding to the arc distances (10.29m and 7.55m). Keeps track of path
length in meters by utilizing getWeight() from the Vertex class and adding each node’s distance to the
running total for each call to A*.

Cost function: Is based on the absolute value difference between the elevation of the current and
potential next node in the path multiplied by the terrain value, all of which is added to the Manhattan
distance (grid) Heuristic. The terrain acts as a multiplying factor for the elevation differential, yielding
the classic g + h score in a conventional A* algorithm.
Heuristic: The Manhattan was chosen over Euclidean for the Heuristic because of the efficiency drain
from computing the Pythagorean theorem, as it would entail calculating the 2nd power for a and b, as
well as the root of those added together.

Season change: To change season maps, I reuse a single BFS function that finds the edge of water, and
then goes inward or outward, coloring the appropriate number of pixels according to depth and color.
Terrain values: For the terrain, I used low numbers (close to 1) for paths and open fields, while giving a
higher multiplier for difficult to traverse areas, such as rough meadows and marsh, which would greatly
slow down an orienteer. Out of bounds, impassible vegetation, and water are all set to inf so the
algorithm will ignore those nodes altogether. For Fall, each of the three forest path types are
incremented by 4, significantly slowing down an orienteer attempting to traverse those areas, and
forces A* to search around them, if possible.

Output: I have the output displayed in main() to terminal that aggregates the cost of all paths as they are
processed in A*, as well as displaying the list of pixels to be colored for the winter and spring seasons.
Main will iterate through all the seasons and inside each season is a for loop that will compute the path
for each course. In order to mark output, each iteration of the inner while loop marks a subsection of
the complete path for the course, and saves it to the same image that is again read on the next iteration.
Inside this for loop is the main while loop that gathers the calls A*, marks the path, and displays output.
