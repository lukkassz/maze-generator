import pygame
import random

# Initialize pygame
pygame.init()

# Window setup
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze generator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cell size
cell_size = 50

# Class Cell
class Cell:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        # Walls: [Top, Right, Bottom, Left]
        self.walls = [True, True, True, True]
        self.visited = False # Check if the cell has been visited

    def check_neighbors(self, grid):
        neighbors = []
        rows = len(grid)
        cols = len(grid[0])

        # Top
        if self.y > 0: # Check if the cel is not on the top row, if it is there is no top neighbor
            top = grid[self.y - 1][self.x] # Get the cell above the current cell so it goes up one row
            if not top.visited: # If the cell above has not been visited add it to the neighbors list
                neighbors.append(top)
        
        # Bottom
        if self.y < rows - 1: # Checking if the cell is not on the botton row like we didt with the top
            bottom = grid[self.y + 1][self.x] # Get the cell below the current cell so it goes down one row
            if not bottom.visited: # Not visited? Add it to the neighbors list
                neighbors.append(bottom)
        
        # Left
        if self.x > 0:
            left = grid[self.y][self.x - 1]
            if not left.visited:
                neighbors.append(left)
        
        # Right
        if self.x < cols -1:
            right = grid[self.y][self.x + 1]
            if not right.visited:
                neighbors.append(right)
                
        return neighbors


    

    def draw(self):
        # Top
        if self.walls[0]:
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.cell_size, self.y), 2)
        # Right
        if self.walls[1]:
            pygame.draw.line(screen, WHITE, (self.x + self.cell_size, self.y), (self.x + self.cell_size, self.y + self.cell_size), 2)
        # Bottom
        if self.walls[2]:
            pygame.draw.line(screen, WHITE, (self.x, self.y + self.cell_size), (self.x + self.cell_size, self.y + self.cell_size), 2)
        # Left
        if self.walls[3]:
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.cell_size), 2)

# Creating empty grid
grid = []

# Columns and rows
cols = screen_width // cell_size 
rows = screen_height // cell_size

# Fill grid with cells
for y in range(rows):
    row = []
    for x in range(cols):
        cell = Cell(x * cell_size, y * cell_size, cell_size)
        row.append(cell)
    grid.append(row)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(BLACK)

    # Draw all cells
    for row in grid:
        for cell in row:
            cell.draw()

    # Update display
    pygame.display.flip()

pygame.quit()
