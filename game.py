import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame.rect import Rect
import sys

pygame.init()

# Define colors
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
RED = pygame.Color("red")

# Set up the screen
screen_width = 500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
screen.fill(BLACK)

# list of rects
maze: list[list[Rect]] = []

# Used for marking tile as wall when searching
# [ 0,  0,  0]
# [-1,  0, -1]
# [-1,  0,  0]

__node_maze = [[0 for i in range(10)] for j in range(10)]

# Game states
START = "start"
END = "end"
WALLS = "walls"
FINDING = "finding"

# Contains path to end tile
path = []


def main():
    global current_state, path, start_pos, end_pos
    start_pos = None
    end_pos = None
    font = pygame.font.Font(None, 36)
    text = font.render("Choose a starting tile  ", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, 100))
    current_state = START

    # run button
    run_button = Button(
        screen, screen_width // 2 - 50, 710, 100, 50, text="Run"
    )
    run_button.inactiveColour = GREEN
    run_button.onClick = lambda: find_shortest_path(start_pos, end_pos)
    
    # reset button
    reset_button = Button(screen, screen_width // 2 - 50, 760, 100, 50, text="Reset")
    reset_button.inactiveColour = RED
    reset_button.onClick = lambda: reset()
    
    while True:
        create_maze()
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == START:
                    start_pos = set_start_position()
                    if start_pos is not None:
                        current_state = END
                        msg = "Choose the ending tile"
                        pygame.draw.rect(screen, pygame.Color('black'), text_rect)
                        text = font.render(msg, True, WHITE)
                elif current_state == END:
                    end_pos = set_end_position()
                    if end_pos is not None:
                        current_state = WALLS
                        msg = "Click tiles for walls"
                        pygame.draw.rect(screen, pygame.Color('black'), text_rect)
                        text = font.render(msg, True, WHITE)
                elif current_state == WALLS:
                    set_wall()
        
        if current_state == FINDING:
            # Could not find a path
            if len(path) == 0:
                msg = "No path found :(("
                pygame.draw.rect(screen, pygame.Color('black'), text_rect)
                text = font.render(msg, True, WHITE)
                reset()
            color_path(path)
            current_state = START
        
        screen.blit(text, text_rect)
        pygame_widgets.update(events)
        pygame.display.flip()


class Node:
    def __init__(self, position: tuple) -> None:
        self.position = position
        self.parent = None
    
    def set_parent(self, node) -> None:
        self.parent = node
    
    def get_parent(self):
        return self.parent


def reset():
    global current_state, start_pos, end_pos, __node_maze, path
    start_pos = end_pos = None
    current_state = START
    for row in maze:
        for rect in row:
            pygame.draw.rect(screen, BLACK, rect)

    __node_maze = [[0 for i in range(10)] for j in range(10)]
    path = []

    return None   


def create_maze():
    block_size = 50
    for i in range(0, 500, block_size):
        row = []
        for j in range(200, 700, block_size):
            rect = pygame.Rect(i, j, block_size, block_size)
            pygame.draw.rect(screen, WHITE, rect, 1)
            row.append(rect)
        maze.append(row)
    return


def set_start_position():
    mouse_position = pygame.mouse.get_pos()
    for row in maze:
        for rect in row:
            if rect.collidepoint(mouse_position):
                pygame.draw.rect(screen, BLUE, rect)
                x, y = mouse_position
                return ((y - 200)//50, x//50)
    return None


def set_end_position():
    mouse_position = pygame.mouse.get_pos()
    for row in maze:
        for rect in row:
            if rect.collidepoint(mouse_position):
                pygame.draw.rect(screen, GREEN, rect)
                x, y = mouse_position
                return ((y - 200)//50, x//50)
    return None


def set_wall():
    mouse_position = pygame.mouse.get_pos()
    for i, row in enumerate(maze):
        for j, rect in enumerate(row):
            if rect.collidepoint(mouse_position):
                # if the rect is already a wall
                # undo it
                if __node_maze[j][i] == -1:
                    __node_maze[j][i] = 0
                    pygame.draw.rect(screen, BLACK, rect)
                    return
                # Turn rect into a wall
                pygame.draw.rect(screen, RED, rect)
                __node_maze[j][i] = -1
                return
    return


def find_shortest_path(start_point, end_point):
    global current_state, path
    if start_point is None or end_point is None:
        return
    current_state = FINDING
    queue = [Node(start_point)]
    visited = set()

    # visited.append(queue[0].position)
    # visited as a dict performs so much 
    # faster then the original list version
    visited.add(queue[0].position)
    while len(queue) > 0:
        current_node = queue.pop(0)
        if current_node.position == end_point:
            while current_node.parent is not None:
                path.insert(0, current_node.position)
                current_node = current_node.get_parent()
            return
        
        y, x = current_node.position
        neighbouring_moves = get_neighbours(y, x)
        for move in neighbouring_moves:
            if move not in visited:
                new_node = Node(move)
                new_node.set_parent(current_node)
                queue.append(new_node)
                
        # visited.append(current_node.position)
        visited.add(current_node.position)

    return None


def get_neighbours(y, x):
    neighbors = []
    if x > 0:
        if __node_maze[y][x-1] != -1:
            neighbors.append((y, x - 1))  # left
    if x < 9:
        if __node_maze[y][x+1] != -1:
            neighbors.append((y, x + 1))  # right
    if y > 0:
        if __node_maze[y-1][x] != -1:
            neighbors.append((y - 1, x))  # up
    if y < 9:
        if __node_maze[y+1][x] != -1:
            neighbors.append((y + 1, x))  # down
    return neighbors


def color_path(path):
    for i, j in path:
        rect = maze[j][i]
        pygame.draw.rect(screen, GREEN, rect)
    return


if __name__ == "__main__":
    main()
