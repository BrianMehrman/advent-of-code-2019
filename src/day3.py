import re
import sys

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def point(self):
        return (self.x, self.y)


def find_intersection(l1, l2):
    (x1, y1), (x2, y2) = l1
    (x3, y3), (x4, y4) = l2

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    # u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    p1 = x1 + t * (x2 -x1)
    p2 = y1 + t * (y2 - y1)

    return (p1, p2)

def isBetween(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > sys.float_info.epsilon:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True

def intersection(lst1, lst2):
    return {tuple(x) for x in lst1 } & {tuple(x) for x in lst2}


def manhatten_distance(x, y):
    return abs(x) + abs(y)

def count_steps(point, wire):
    return wire.index(point) + 1


class IntersectionTool():
    DIRECTION_MAP = {
        "U": (0 , 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0)
    }

    def __init__(self, wires):
        self.wires = wires
        self.wire_map = {}

    def read(self, direction):
        match = re.search("([UDLR])(\d+)", direction)

        if match:
            x, y = self.DIRECTION_MAP[match[1]]
            distance = int(match[2])

            return  (x * distance, y * distance, x or 1, y or 1)
        else:
            raise Exception("Direction failed to parse", direction)

    def walk(self, wire):
        position = Vector(0,0)
        wire_points = []

        for direction in wire:
            x, y, dx, dy = self.read(direction)

            for _x in range(0, x + dx, dx):
                for _y in range(0, y + dy, dy):
                    if [_x, _y] != [0, 0]:
                        wire_points.append([position.x + _x, position.y + _y])

            position.move(x, y)

        return wire_points

    def trace(self):
        for wire_id in range(len(self.wires)):
            wire_points = self.walk(self.wires[wire_id])
            self.wire_map[wire_id] = wire_points[:]


    def closest_intersection(self):
        self.trace()
        wire_a = self.wire_map[0]
        wire_b = self.wire_map[1]

        intersecting_points = intersection(wire_a, wire_b)
        # distances = [manhatten_distance(point[0], point[1]) for point in intersecting_points if point[0] != 0 and point[1] != 0]
        distances = [count_steps(list(point), wire_a) + count_steps(list(point), wire_b) for point in intersecting_points]

        if distances:
            return min(distances)
        else:
            return "Nothing"

    # def calc_intersections(self):
    #     wire_a = self.wire_points[0]
    #     wire_b = self.wire_points[1]
    #     intersections = []
    #     for i in len(wire_a) - 1:
    #         for j in len(wire_b) - 1:
    #             l1 = [wire_a[i], wire_a[i + 1]]
    #             l2 = [wire_b[j], wire_b[j + 1]]

    #             px, py = find_intersection(l1, l2)

    #             p = Vector(px, py)

    #             (x1, y1), (x2, y2) = l1
    #             (x3, y3), (x4, y4) = l2

    #             a = Vector(x1, y1)
    #             b = Vector(x2, y2)
    #             c = Vector(x3, y3)
    #             d = Vector(x4, y4)

    #             if isBetween(a, b , p) and isBetween(c, d, p):
    #                 intersections.append((px, py))

    #     return intersections

if __name__ == "__main__":
    data = open("./data/day3.txt")
    wires = [ line.rstrip().split(",") for line in data.readlines()]

    tool = IntersectionTool(wires)
    print(tool.closest_intersection())


