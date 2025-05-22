import pygame, sys, random, time

# Initialize pygame
pygame.init()
screen_width = 800
screen_height = 600
cell_size = 40
cols = screen_width // cell_size
rows = screen_height // cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (250, 120, 60)
YELLOW = (255, 255, 0)

# Cell class
class Cell:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * cell_size
        self.y = y * cell_size
        self.walls = [True, True, True, True]  # Top, Right, Bottom, Left
        self.visited = False

    def check_neighbors(self, grid):
        neighbors = []
        if self.grid_y > 0:
            top = grid[self.grid_y - 1][self.grid_x]
            if not top.visited:
                neighbors.append(top)
        if self.grid_y < rows - 1:
            bottom = grid[self.grid_y + 1][self.grid_x]
            if not bottom.visited:
                neighbors.append(bottom)
        if self.grid_x > 0:
            left = grid[self.grid_y][self.grid_x - 1]
            if not left.visited:
                neighbors.append(left)
        if self.grid_x < cols - 1:
            right = grid[self.grid_y][self.grid_x + 1]
            if not right.visited:
                neighbors.append(right)
        return neighbors

    def draw(self):
        if self.walls[0]:
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + cell_size, self.y), 2)
        if self.walls[1]:
            pygame.draw.line(screen, WHITE, (self.x + cell_size, self.y), (self.x + cell_size, self.y + cell_size), 2)
        if self.walls[2]:
            pygame.draw.line(screen, WHITE, (self.x, self.y + cell_size), (self.x + cell_size, self.y + cell_size), 2)
        if self.walls[3]:
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + cell_size), 2)

def remove_walls(a, b):
    dx = a.grid_x - b.grid_x
    dy = a.grid_y - b.grid_y
    if dx == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif dx == -1:
        a.walls[1] = False
        b.walls[3] = False
    if dy == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif dy == -1:
        a.walls[2] = False
        b.walls[0] = False

def generate_maze():
    stack = []
    current = grid[0][0]
    current.visited = True
    total = rows * cols
    visited = 1
    while visited < total:
        neighbors = current.check_neighbors(grid)
        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
            current.visited = True
            visited += 1
        elif stack:
            current = stack.pop()

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.size = cell_size - 10
        self.color = ORANGE

    def draw(self):
        screen_x = self.grid_x * cell_size + 5
        screen_y = self.grid_y * cell_size + 5
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.size, self.size))

    def move(self, direction, grid):
        current = grid[self.grid_y][self.grid_x]
        if direction == "LEFT" and not current.walls[3] and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == "RIGHT" and not current.walls[1] and self.grid_x < cols - 1:
            self.grid_x += 1
        elif direction == "UP" and not current.walls[0] and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == "DOWN" and not current.walls[2] and self.grid_y < rows - 1:
            self.grid_y += 1

    def get_cell(self):
        return self.grid_x, self.grid_y

class ClockTimer:
    def __init__(self):
        self.start = time.time()
        self.font = pygame.font.SysFont("monospace", 24)

    def draw(self):
        elapsed = int(time.time() - self.start)
        mins = elapsed // 60
        secs = elapsed % 60
        text = self.font.render(f"Time: {mins:02}:{secs:02}", True, YELLOW)
        screen.blit(text, (10, 10))

# Grid setup
grid = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
generate_maze()

# Game objects
player = Player(0, 0)
goal_cell = grid[rows - 1][cols - 1]
clock_timer = ClockTimer()
font = pygame.font.SysFont("impact", 50)
goal_img = pygame.Surface((cell_size, cell_size))
goal_img.fill((0, 200, 0))

# Game loop
running = True
won = False
FPS = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not won:
            if event.key == pygame.K_LEFT:
                player.move("LEFT", grid)
            elif event.key == pygame.K_RIGHT:
                player.move("RIGHT", grid)
            elif event.key == pygame.K_UP:
                player.move("UP", grid)
            elif event.key == pygame.K_DOWN:
                player.move("DOWN", grid)

    # Draw maze
    for row in grid:
        for cell in row:
            cell.draw()

    # Draw goal
    screen.blit(goal_img, (goal_cell.x, goal_cell.y))

    # Draw player
    player.draw()

    # Draw timer
    if not won:
        clock_timer.draw()

    # Check win
    player_cell_x, player_cell_y = player.get_cell()
    if player_cell_x == cols - 1 and player_cell_y == rows - 1:
        won = True
        win_text = font.render("You won!", True, ORANGE)
        screen.blit(win_text, (screen_width // 2 - 100, screen_height // 2 - 25))

    pygame.display.flip()
    FPS.tick(60)

pygame.quit()
