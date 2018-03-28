MOVE_COST = {1:10.29,
        2:10.29,
        3:7.55,
        4:7.55}

class Graph:
    def __init__(self):
        self.vertices = {}

    def addVertex(self, point, terrain=0, elev=0):
        newVertex = Vertex(point, terrain, elev)
        self.vertices[point] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertices

    def getVertices(self):
        return list(self.vertices.keys())

    def cost(self, current, next):
        return abs(next.elev - current.elev) * next.terrain

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    __slots__ = 'point', 'connectedTo', 'elev', 'terrain'

    def __init__(self, point, terrain, elev):
        self.point = point
        self.elev = elev
        self.terrain = terrain
        self.connectedTo = {}

    def __lt__(self, other):
        return True if self.terrain < other.terrain else False

    def addNeighbor(self, nbr, childID):
        weight = MOVE_COST[childID]
        self.connectedTo[nbr] = weight # 10.29m or 7.55m

    def getConnections(self):
        return self.connectedTo.keys()

    def __str__(self):
        return 'Point: ' + str(self.point) + \
                ' Elev: ' + str(self.elev) + ' Terrain: ' + str(self.terrain)

    def getPoint(self):
        return self.point

    def getWeight(self, other):
        return self.connectedTo[other]