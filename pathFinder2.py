from tkinter import Tk, messagebox
import pygame
import sys

window_width = 800
window_height = 600

window = pygame.display.set_mode((window_width, window_height))

cols = 25
rows = 25

box_width = window_width / cols
box_height = window_height / rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = 0
        self.end = 0
        self.obstacle = 0
        self.color = (50, 50, 50)
        self.visited = False
        self.queued = False
        self.neighbors = []
        self.previous = None

    def show(self, window, color):
        pygame.draw.rect(window, color, (self.x * box_width,
                         self.y * box_height, box_width - 2, box_height - 2))

    def setStart(self):
        self.start = 1

    def setEnd(self):
        self.end = 1

    def setObstacle(self):
        self.obstacle = 1

    def addNeighbors(self):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])


# Create Grid with 2D Array
for i in range(cols):
    arr = []  # Create empty array for each row in the grid
    for j in range(rows):
        # Append each box to the array for each row in the grid. This creates a 2D array of boxes that can be accessed by grid[i][j]
        arr.append(Box(i, j))
    grid.append(arr)  # Append the array to the grid


# set neighbours
for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors()

start_box = None

def main():

    begin_search = False
    target_box_set = False
    target_box = None
    searching = True
    # start_box = grid[0][0]
    start_box = None

    while True:
        # box = Box(0, 0)
        # box.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # window.fill((0, 0, 0))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # # Get Mouse Position
        if event.type == pygame.MOUSEBUTTONDOWN and not target_box_set:
            pos = pygame.mouse.get_pos()
            x = int(pos[0] // box_width)
            y = int(pos[1] // box_height)
            if event.button == 3:
                target_box = grid[x][y]
                target_box.setEnd()
                target_box_set = True

            if event.button == 1 and start_box == None:
                start_box = grid[x][y]
                start_box.setStart()
                start_box.visited = True
                queue.append(start_box)

        if event.type == pygame.MOUSEMOTION:  # or event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = int(pos[0] // box_width)
            y = int(pos[1] // box_height)
            box = grid[x][y]
            if event.buttons[0] == 1 and not target_box_set:
                grid[x][y].setObstacle()


        if keys[pygame.K_SPACE] and target_box_set:
            begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True

                if current_box == target_box:
                    print("Target Found")
                    searching = False
                    path.append(current_box)

                else:
                    for neighbor in current_box.neighbors:
                        if neighbor == target_box:
                            print("Target Found")
                            searching = False
                            while current_box != start_box:
                                path.append(current_box)
                                current_box = current_box.previous
                            # show start box in different color
                            start_box.show(window, (0, 255, 0))
                        elif not neighbor.obstacle and not neighbor.queued:
                            neighbor.queued = True
                            neighbor.previous = current_box
                            queue.append(neighbor)

        for i in range(cols):
            for j in range(rows):
                # Get the box at the current position in the grid array and store it in the box variable
                box = grid[i][j]
                box.show(window, (50, 50, 50))
                if box.start == 1:
                    box.show(window, (48, 227, 202))  # rgb(48, 227, 202)
                if box.obstacle == 1:
                    box.show(window, (64, 81, 78))  # rgb(64, 81, 78)
                if box.end == 1:
                    box.show(window, (228, 249, 245))  # rgb(228, 249, 245)
                if box.visited:
                    box.show(window, (0, 255, 0))  # rgb(0, 255, 0)
                if box.queued:
                    if box == start_box:
                        box.show(window, (0, 255, 255)) # rgb(0, 255, 255)
                    else:
                        box.show(window, (255, 0, 0))  # rgb(255, 0, 0)
                if box in path:
                    box.show(window, (48, 27, 202))  # rgb(78, 27, 202)
                    
                    
                if not searching:
                    box.show(window, (50, 50, 50)) # rgb(50, 50, 50)
                    if box in path:
                        box.show(window, (48, 27, 202))  # rgb(78, 27, 202)
                    if box.queued:
                        if box == start_box:
                            box.show(window, (0, 255, 0)) # rgb(0, 255, 0)
                    if box.obstacle == 1:
                        box.show(window, (64, 81, 78))  # rgb(64, 81, 78)
                    if box.end == 1:
                        box.show(window, (228, 249, 245))  # rgb(228, 249, 245)
                    

        pygame.display.flip()


main()
