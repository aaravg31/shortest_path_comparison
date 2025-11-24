import pygame
from typing import Tuple, Dict, List, Any

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

class Grid:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = self.make_grid()
        self.start = None
        self.end = None

    def make_grid(self):
        grid = []
        gap = self.width // self.rows
        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                node = Node(i, j, gap, self.rows)
                grid[i].append(node)
        return grid

    def draw_grid_lines(self, win):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(win, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, self.width))

    def draw(self, win, shortcuts=None):
        win.fill(WHITE)
        for row in self.grid:
            for node in row:
                node.draw(win)
        
        # Draw shortcuts if provided
        if shortcuts:
            for (u, v) in shortcuts:
                u_node = self.get_node(u[0], u[1])
                v_node = self.get_node(v[0], v[1])
                if u_node and v_node:
                    # Draw a yellow/gold line from center of u to center of v
                    start_pos = (u_node.x + u_node.width // 2, u_node.y + u_node.width // 2)
                    end_pos = (v_node.x + v_node.width // 2, v_node.y + v_node.width // 2)
                    pygame.draw.line(win, (255, 215, 0), start_pos, end_pos, 3)  # Gold color, 3px wide
        
        self.draw_grid_lines(win)
        pygame.display.update()

    def get_clicked_pos(self, pos):
        gap = self.width // self.rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

    def get_node(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.rows:
            return self.grid[row][col]
        return None

    def clear(self):
        self.start = None
        self.end = None
        self.grid = self.make_grid()

    def clear_path(self):
        for row in self.grid:
            for node in row:
                if not (node.is_start() or node.is_end() or node.is_barrier()):
                    node.reset()

    def to_adjacency_dict(self) -> Dict[Any, List[Tuple[Any, float]]]:
        """
        Convert grid to adjacency list: {node: [(neighbor, weight), ...]}
        Nodes (row, col) tuples
        """
        graph = {}
        for row in self.grid:
            for node in row:
                if node.is_barrier():
                    continue
                
                node.update_neighbors(self.grid)
                u = (node.row, node.col)
                graph[u] = []
                
                for neighbor in node.neighbors:
                    v = (neighbor.row, neighbor.col)
                    # Default weight of 1
                    graph[u].append((v, 1.0))
        return graph
