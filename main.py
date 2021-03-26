import pygame as pg


class Labyrinth:
    # Default Start Position
    x_start = 2
    y_start = 2

    # Default Goal Position
    x_goal = 23
    y_goal = 24

    # Default window/field settings
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 700
    BLOCK_SIZE = 25
    BLOCK_MIDDLE_SIZE = BLOCK_SIZE / 2
    SPEED = 50  # Defines how many milliseconds a step has to take, till the next step can be done
    X_FIELD_DIMENSION = 0
    Y_FIELD_DIMENSION = 0

    # RGB Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)

    WINDOW = None
    CLOCK = None
    isGameActive = True

    # Walls
    WALLS = None
    BFS_WALLS = None

    clock = pg.time.Clock()

    # Constructor, overwrite default values
    def __init__(self, speed, xStart, yStart, xEnd, yEnd):
        # Overwrite default values
        self.SPEED = speed
        self.x_start = xStart
        self.y_start = yStart
        self.x_goal = xEnd
        self.y_goal = yEnd

        # Check if start position is not a wall otherwise quit
        self.readFieldData()
        self.isStartOrGoalPositionAWall()
        self.buildBFSWalls()
        self.initialize()

    # Initialize pygame

    def initialize(self):
        pg.init()
        self.WINDOW = pg.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption("Algorithm based self solving maze")
        counter = 0

        while self.isGameActive:
            for event in pg.event.get():
                # Set isGameActive to False because user pressed quit
                if event.type == pg.QUIT:
                    self.isGameActive = False
            # Set background color
            if(counter == 0):
                self.WINDOW.fill(self.WHITE)
                # Draw all walls, draw start position, draw goal position
                self.drawGoalPosition()
                self.drawStartPosition()
                self.drawWalls()
                pg.display.update()
                self.makeSteps()
                counter += 1

    # Read file for building the maze
    def readFieldData(self):
        with open("field.txt", 'rt') as file:
            # X dimension of field
            x_dimension = int(file.readline())
            self.X_FIELD_DIMENSION = x_dimension
            # Y dimension of field
            y_dimension = int(file.readline())
            self.Y_FIELD_DIMENSION = y_dimension
            # Checking if the given values for the field dimensions are valid, closing if not
            if(self.checkForValidDimensions() == False):
                exit()
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
        pg.draw.circle(self.WINDOW, self.GREEN, (self.x_start * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE,
                                                 self.y_start * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE), 6, 0)

    # Draw goal position point
    def drawGoalPosition(self):
        pg.draw.circle(self.WINDOW, self.RED, (self.x_goal * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE,
                                               self.y_goal * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE), 6, 0)

    # Draw shortest path line
    def drawPathLine(self, x, y):
        x_coordinate = x * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
        y_coordinate = y * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
        pg.draw.line(self.WINDOW, self.GREEN,
                     (x_coordinate, y_coordinate + 20), (x_coordinate, y_coordinate + 20), 6)

    # Check if start or goal position is a wall (1 == wall, 0 == way/free space)
    def isStartOrGoalPositionAWall(self):
        res = self.WALLS[self.y_start][self.x_start]
        if res == 1:
            print(
                "ERROR: Your start position is a wall. Please choose another x and y coordinate.")
            # Close program
            exit()
        res = self.WALLS[self.y_goal][self.x_goal]
        if res == 1:
            print(
                "ERROR: Your goal position is a wall. Please choose another x and y coordinate.")
            # Close program
            exit()

    """
    BFS algorithm to solve and find the exit in the maze
    create matrix with 0s by size of X_FIELD_DIMENSION x Y_FIELD_DIMENSION
    1 => our starting point from x_start and y_start (self.walls[y][x])
    Everywhere around 1 we put 2 , if there is no wall
    Everywhere around 2 we put 3 , if there is no wall
    and so on…
    once we put a number at the ending point, we stop. This number is actually the minimal path length
    """

    def buildBFSWalls(self):
        walls_with_zeros = [
            [0 for _ in range(self.X_FIELD_DIMENSION)] for _ in range(self.Y_FIELD_DIMENSION)]
        # insert 1 which is our starting point
        walls_with_zeros[self.y_start][self.x_start] = 1
        self.BFS_WALLS = walls_with_zeros

    def makeSteps(self):
        k = 0
        while self.BFS_WALLS[self.y_goal][self.x_goal] == 0:
            k += 1
            self.makeStep(k)
        self.drawShortestPath()

    def drawShortestPath(self):
        shortest_path = self.getShortedPath()
        for coordinates in shortest_path:
            self.drawPathLine(coordinates[0], coordinates[1])
            pg.display.flip()

    def getShortedPath(self):
        BFS_MAZE = self.BFS_WALLS
        i, j = (24, 23)
        k = BFS_MAZE[i][j]
        the_path = [(i, j)]
        while k > 1:
            if i > 0 and BFS_MAZE[i - 1][j] == k-1:
                i, j = i-1, j
                the_path.append((i, j))
                k -= 1
            elif j > 0 and BFS_MAZE[i][j - 1] == k-1:
                i, j = i, j-1
                the_path.append((i, j))
                k -= 1
            elif i < len(BFS_MAZE) - 1 and BFS_MAZE[i + 1][j] == k-1:
                i, j = i+1, j
                the_path.append((i, j))
                k -= 1
            elif j < len(BFS_MAZE[i]) - 1 and BFS_MAZE[i][j + 1] == k-1:
                i, j = i, j+1
                the_path.append((i, j))
                k -= 1
        return the_path

    def makeStep(self, k):
        # m => 0 matrix
        # a => original matrix
        BFS_MAZE = self.BFS_WALLS
        ORIGINAL_MAZE = self.WALLS
        for i in range(len(BFS_MAZE)):
            for j in range(len(BFS_MAZE[i])):
                if BFS_MAZE[i][j] == k:
                    if i > 0 and BFS_MAZE[i-1][j] == 0 and ORIGINAL_MAZE[i-1][j] == 0:
                        BFS_MAZE[i-1][j] = k + 1
                        pg.draw.circle(self.WINDOW, self.BLUE, (j * self.BLOCK_SIZE + 12,
                                                                i * self.BLOCK_SIZE + 12), 6, 0)

                    if j > 0 and BFS_MAZE[i][j-1] == 0 and ORIGINAL_MAZE[i][j-1] == 0:
                        BFS_MAZE[i][j-1] = k + 1
                        pg.draw.circle(self.WINDOW, self.BLUE, (j * self.BLOCK_SIZE + 12,
                                                                i * self.BLOCK_SIZE + 12), 6, 0)

                    if i < len(BFS_MAZE)-1 and BFS_MAZE[i+1][j] == 0 and ORIGINAL_MAZE[i+1][j] == 0:
                        BFS_MAZE[i+1][j] = k + 1
                        pg.draw.circle(self.WINDOW, self.BLUE, (j * self.BLOCK_SIZE + 12,
                                                                i * self.BLOCK_SIZE + 12), 6, 0)

                    if j < len(BFS_MAZE[i])-1 and BFS_MAZE[i][j+1] == 0 and ORIGINAL_MAZE[i][j+1] == 0:
                        BFS_MAZE[i][j+1] = k + 1
                        pg.draw.circle(self.WINDOW, self.BLUE, (j * self.BLOCK_SIZE + 12,
                                                                i * self.BLOCK_SIZE + 12), 6, 0)
                    self.drawStartPosition()
                    self.drawGoalPosition()
                    pg.display.update()
                    self.clock.tick(self.SPEED)

    # Checking if given field dimensions are valid. Checking for: emptiness, smaller than 10, if format is between 16:9 / 9:16

    def checkForValidDimensions(self):
        SIXTEEN_BY_NINE_CONSTANT = 1.78
        X_DEVIDED_BY_Y = self.X_FIELD_DIMENSION/self.Y_FIELD_DIMENSION
        Y_DEVIDED_BY_X = self.Y_FIELD_DIMENSION/self.X_FIELD_DIMENSION
        if (self.X_FIELD_DIMENSION or self.Y_FIELD_DIMENSION) == 0:
            print("WARNING: Your maze dimensions are empty.")
            return False
        elif (self.X_FIELD_DIMENSION < 10 or self.Y_FIELD_DIMENSION < 10):
            print("WARNING: Minimum size is 10 blocks by 10 blocks, so atleast {fDIMENSION_BY_BLOCKS} by {fDIMENSION_BY_BLOCKS}.").format(
                fDIMENSION_BY_BLOCKS=10*self.BLOCK_SIZE)
            return False
        elif (X_DEVIDED_BY_Y > SIXTEEN_BY_NINE_CONSTANT or Y_DEVIDED_BY_X > SIXTEEN_BY_NINE_CONSTANT):
            print(
                "WARNING: Smallest possible format for field dimensions are 16:9 or 9:16.")
            return False


Game = Labyrinth(75, 1, 1, 21, 23)
