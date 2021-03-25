"""
TODOS:
- Algorithmus implementieren der Ziel (x_goal und y_goal findet)
- Angegebene Dimensionen auf Sinn überprüfen (70:30/16:9)
- Geschwindigkeit über Parameter bestimmen (pygame clock)
- 10 Bonuspunkte, wenn Programm kürzesten Pfad anzeigt von Start zu Ziel
"""

import pygame as pg


class Labyrinth:
    # Default Start Position
    x_start = 0
    y_start = 0

    # Default Goal Position
    x_goal = 18
    y_goal = 0

    # Default window/field settings
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 700
    BLOCK_SIZE = 25
    BLOCK_MIDDLE_SIZE = BLOCK_SIZE / 2
    SPEED = 20
    X_FIELD_DIMENSION = 0
    Y_FIELD_DIMENSION = 0

    # RGB Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)

    WINDOW = None
    CLOCK = None
    isGameActive = True

    # Walls
    WALLS = None

    # Constructor, overwrite default values
    def __init__(self, speed, x, y):
        # Overwrite default values
        self.speed = speed
        self.x_start = x
        self.y_start = y

        # Check if start position is not a wall otherwise quit
        self.readFieldData()
        self.isStartPositionAWall()
        self.initialize()
        self.searchExit()

    # Initialize pygame
    def initialize(self):
        pg.init()
        self.WINDOW = pg.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption("Algorithm based self solving maze")

        while self.isGameActive:
            for event in pg.event.get():
                # Set isGameActive to False because user pressed quit
                if event.type == pg.QUIT:
                    self.isGameActive = False
            # Set background color
            self.WINDOW.fill(self.WHITE)
            # Draw all walls, draw start position, draw goal position
            self.drawWalls()
            self.drawStartPosition()
            self.drawGoalPosition()
            pg.display.update()

    # Read file for building the maze
    def readFieldData(self):
        with open("field.txt", 'rt') as file:
            # X dimension of field
            x_dimension = int(file.readline())
            self.X_FIELD_DIMENSION = x_dimension
            # Y dimension of field
            y_dimension = int(file.readline())
            self.Y_FIELD_DIMENSION = y_dimension
            # Read rows and create always a new array until \n/line breaks come in
            rows = file.read().splitlines()
            cols = []
            for line in rows:
                # splitlines() creates string arrays
                # convert array values from type string to int
                lineToInt = list(map(int, line.split()))
                cols.append(lineToInt)
            self.WALLS = cols

    # Draw all walls
    def drawWalls(self):
        for line, lineValue in enumerate(self.WALLS):
            for column, columnValue in enumerate(lineValue):
                if columnValue == 1:
                    xPosStart = (column) * self.BLOCK_SIZE
                    xPosEnd = xPosStart + self.BLOCK_SIZE
                    # +12 weil draw.line von dem pixel aus + die hälfte nach unten zeichnet und + die hälfte nach unten, da 25 ein Block ist also +12 hier mal, sonst am oberen Rand nur hälfte zusehen
                    yPos = line * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
                    self.drawWall(xPosStart, yPos, xPosEnd)
        pg.display.update()

    # Draw wall
    def drawWall(self, x_start, y_current, x_end):
        pg.draw.line(self.WINDOW, self.BLACK, (x_start, y_current),
                     (x_end, y_current), self.BLOCK_SIZE)

    # Draw start position point
    def drawStartPosition(self):
        pg.draw.circle(self.WINDOW, self.GREEN, (self.x_start * self.BLOCK_SIZE + 12,
                                                 self.y_start * self.BLOCK_SIZE + 12), 6, 0)

    # Draw goal position point
    def drawGoalPosition(self):
        pg.draw.circle(self.WINDOW, self.RED, (self.x_goal * self.BLOCK_SIZE + 12,
                                               self.y_goal * self.BLOCK_SIZE + 12), 6, 0)

    # Check if start position is a wall (1 == wall, 0 == way/free space)
    def isStartPositionAWall(self):
        res = self.WALLS[self.y_start][self.x_start]
        if res == 1:
            print(
                "ERROR: Your start position is a wall. Please choose another x and y coordinate.")
            # Close program
            exit()

    """
    BFS algorithm to solve and find the exit in the maze
    create matrix with 0s by size of X_FIELD_DIMENSION x Y_FIELD_DIMENSION
    1 => our starting point from x_start and y_start (self.walls[y][x])

    """

    def searchExit(self):
        walls_with_zeros = [
            [0 for i in range(self.X_FIELD_DIMENSION)] for j in range(self.Y_FIELD_DIMENSION)]
        # insert 1 which is our starting point
        walls_with_zeros[self.y_start][self.x_start] = 1
        print(walls_with_zeros)

    def checkForValidDimensions(self):
        if (self.X_FIELD_DIMENSION or self.Y_FIELD_DIMENSION) == 0:
            print("WARNING: Your maze dimensions are empty.")


Game = Labyrinth(25, 1, 1)
