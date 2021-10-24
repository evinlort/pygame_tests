import random
from typing import List, Tuple

import pygame

FPS = 5
SIZE = 20
H = 801
W = 1201

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)


class Cell:
    def __init__(self, i: int, j: int, visited: bool, walls: List, neighbours=None):
        if neighbours is None:
            neighbours = []
        self.i = i
        self.j = j
        self.visited = visited
        self.walls = walls
        self.neighbours = neighbours


class CellGrid:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.cells = list()
        self.build_grid()

    def build_grid(self):
        for i in range(self.cols):
            for j in range(self.rows):
                cell = Cell(i, j, False, [True, True, True, True])
                self.cells.append(cell)

    def check_neighbours(self, cell: Cell) -> Tuple[bool, List[Cell]]:
        neighbours = []

        if cell.j > 0 and (not self.cells[index(cell.i, cell.j - 1)].visited):
            neighbours.append(self.cells[index(cell.i, cell.j - 1)])

        if cell.i < cols - 1 and (not self.cells[index(cell.i + 1, cell.j)].visited):
            neighbours.append(self.cells[index(cell.i + 1, cell.j)])

        if cell.j < rows - 1 and (not self.cells[index(cell.i, cell.j + 1)].visited):
            neighbours.append(self.cells[index(cell.i, cell.j + 1)])

        if cell.i > 0 and (not self.cells[index(cell.i - 1, cell.j)].visited):
            neighbours.append(self.cells[index(cell.i - 1, cell.j)])

        if len(neighbours) > 0:
            return True, neighbours
        else:
            return False, neighbours

    def choose_neighbours(self, cell):
        boolean, neighbours = self.check_neighbours(cell)
        if boolean:
            return random.choice(neighbours)

    def __call__(self):
        return self.cells


class Drawer:
    def __init__(self, grid):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((W, H))
        self.stack = list()
        self.grid = grid()
        self.grid_object = grid
        self.draw()
        self.carve_maze()

    def draw_rect(self, i, j, s):
        pygame.draw.rect(self.screen, PURPLE, (i * SIZE + 1, j * SIZE + 1, s - 1, s - 1), 0)

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(len(self.grid)):
            cell = self.grid[i]
            '''top'''
            if cell.walls[0]:
                pygame.draw.line(self.screen, WHITE, index_to_location(cell.i, cell.j),
                                 index_to_location(cell.i + 1, cell.j))
            '''right'''
            if cell.walls[1]:
                pygame.draw.line(self.screen, WHITE, index_to_location(cell.i + 1, cell.j),
                                 index_to_location(cell.i + 1, cell.j + 1))
            '''bottom'''
            if cell.walls[2]:
                pygame.draw.line(self.screen, WHITE, index_to_location(cell.i + 1, cell.j + 1),
                                 index_to_location(cell.i, cell.j + 1))
            '''left'''
            if cell.walls[3]:
                pygame.draw.line(self.screen, WHITE, index_to_location(cell.i, cell.j + 1),
                                 index_to_location(cell.i, cell.j))
        pygame.display.update()

    def carve_maze(self):
        visited = 1
        current_cell = self.grid[0]
        current_cell.visited = True
        while visited < (rows * cols):
            if self.grid_object.check_neighbours(current_cell)[0]:
                next_cell = self.grid_object.choose_neighbours(current_cell)
                next_cell.visited = True

                self.stack.append(current_cell)

                remove_walls(current_cell, next_cell)

                current_cell = next_cell
                visited += 1
            elif len(self.stack) > 0:
                current_cell = self.stack.pop()
            self.draw()
            self.draw_rect(current_cell.i, current_cell.j, SIZE)
            pygame.display.update()
            pygame.time.delay(1)


def index(i, j):
    return j + i * rows


def index_to_location(i, j):
    return [i * SIZE, j * SIZE]


def remove_walls(a, b):
    if a.i - b.i == 1:
        a.walls[3] = False
        b.walls[1] = False
    if a.i - b.i == -1:
        a.walls[1] = False
        b.walls[3] = False
    if a.j - b.j == 1:
        a.walls[0] = False
        b.walls[2] = False
    if a.j - b.j == -1:
        a.walls[2] = False
        b.walls[0] = False


if __name__ == "__main__":
    rows = int(H / SIZE)
    cols = int(W / SIZE)
    cells = CellGrid(cols, rows)
    Drawer(cells)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
