import pygame
import time

from queue import PriorityQueue, deque

"""
Sources:
http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
"""

SN = 0
EN = 1
WA = 2
NN = 3

START = (255, 0, 0)
NORMAL = (100, 100, 100)
WALL = (255, 255, 255)
END = (0, 0, 255)

FINAL = (111, 7, 214)



class Tile:
    def __init__(self, x, y, w, h, tt):
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = (x // w, y // h)
        self.color = (255, 255, 255)
        self.visited = False
        self.ttype = tt
        self.parent = None
        self.final = False

    def reset(self):
        self.visited = False
        self.final = False
        if self.ttype not in [SN, EN]:
            self.ttype = NN
    
    @property
    def ttype(self):
        return self._ttype
    
    @ttype.setter
    def ttype(self, value):
        if value == SN:
            self.color = START
        elif value == EN:
            self.color = END
        elif value == WA:
            self.color = WALL
        elif value == NN:
            self.color = NORMAL
        self._ttype = value

    def render(self, surface):
        """Render the tile"""
        # if self.rect.topleft == (0, 0):
            # print(self.color, self.ttype)
            # pass
        if self.final and self.ttype not in [SN, EN]: pygame.draw.rect(surface, FINAL, self.rect)
        else: pygame.draw.rect(surface, self.color, self.rect)
        if self.visited:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 3)


class Node:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.grid = grid
        self.parent = None

        self.g = 0
        self.h = 0
        self.f = 0


class Grid:
    WIDTH = 40
    HEIGHT = 40

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [
            [Tile(x, y, self.WIDTH, self.HEIGHT, NN) for x in range(0, self.cols * self.WIDTH, self.WIDTH)] for y in range(0, self.rows * self.HEIGHT, self.HEIGHT)
        ]
        # important nodes
        self._start = (0, 0)
        self._end = (0, 0)

        self.start = (0, 0)
        self.end = (self.cols - 1, self.rows - 1)

        self._solution = []

    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self, value):
        self.grid[self._start[1]][self._start[0]].ttype = NN
        self._start = value
        self.grid[self._start[1]][self._start[0]].ttype = SN
        print(self._start)
    
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self.grid[self._end[1]][self._end[0]].ttype = NN
        self._end = value
        self.grid[self._end[1]][self._end[0]].ttype = EN

    def get_node(self, x, y):
        """Get the node at the given position"""
        return self.grid[y][x]

    def render(self, surface):
        """Render the grid"""
        for row in self.grid:
            for tile in row:
                tile.render(surface)
    
    def reset(self):
        # reset map
        for row in self.grid:
            for tile in row:
                tile.reset()

    def solve(self):
        """Solve the grid using a-star algorithm"""

        # start the algorithm
        print("start")
        open_set = []
        closed_set = []
        open_set.append((0, Node(self.start[0], self.start[1], self)))

        while open_set:
            open_set.sort(key=lambda x: x[0])
            current = open_set.pop(0)[1]
            
            # visited
            if self.get_node(current.x, current.y).visited: continue
            # time.sleep(1/60)
            closed_set.append(current)
            # set the node to be visited
            self.grid[current.y][current.x].visited = True

            # if it is the goal
            if current.pos == self.end:
                self.reconstruct_path(closed_set)
                break
            
            # generate some kids
            for npos in self.get_neighbors(current.pos):
                # if already vis
                if npos in closed_set: continue
                # check if it is a wall
                if self.get_node(npos[0], npos[1]).ttype == WA: continue
                # calculate some values
                nnode = Node(npos[0], npos[1], self)
                nnode.parent = current
                nnode.g = current.g + 1
                nnode.h = ((nnode.x - self.end[0]) ** 2) + ((nnode.y - self.end[1]) ** 2)
                nnode.f = nnode.g + nnode.h
                # cool
                # now we do some checks
                for i in open_set:
                    if i[1] == nnode and nnode.g > i[1].g:
                        continue

                # add to open list
                open_set.append((nnode.f, nnode))
            time.sleep(1/60)
        
        print("dopne")

    def reconstruct_path(self, closed_set):
        """Reconstruct the path"""
        current = closed_set[-1]
        while current:
            self.grid[current.y][current.x].final = True
            current = current.parent
            time.sleep(1/60)

    def get_neighbors(self, pos):
        """Get the neighbors of the given position"""
        # for x in range(max(0, pos[0] - 1), min(self.cols, pos[0] + 2)):
        #     for y in range(max(0, pos[1] - 1), min(self.rows, pos[1] + 2)):
        #         if (x, y) != pos:
        #             yield (x, y)
        for dx, dy in ([0, 1], [1, 0], [0, -1], [-1, 0]):
            x = pos[0] + dx
            y = pos[1] + dy
            if 0 <= x < self.cols and 0 <= y < self.rows:
                yield (x, y)



