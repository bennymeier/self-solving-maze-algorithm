import pygame as pg


class Labyrinth:
    # Default start position
    x_start = 2
    y_start = 2

    # Default goal position
    x_goal = 23
    y_goal = 24

    # Default window/field settings
    WINDOW_TITLE = "Self solving maze based on an algorithm by LouisB, EmreG, JonasK, BenjaminM"
    WINDOW_WIDTH = 750
    WINDOW_HEIGHT = 700
    BLOCK_SIZE = 25
    BLOCK_MIDDLE_SIZE = BLOCK_SIZE / 2
    # Defines how many milliseconds a step has to take, till the next step can be done
    SPEED = 50
    X_FIELD_DIMENSION = 0
    Y_FIELD_DIMENSION = 0

    # RGB Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 87, 51)
    GREEN = (0, 128, 0)
    BLUE = (7, 67, 182)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 127, 80)

    # General
    WINDOW = None
    CLOCK = None
    isGameActive = True

    # Walls
    WALLS = []
    BFS_WALLS = []

    clock = pg.time.Clock()

    # Constructor, overwrite default values
    def __init__(self, speed, xStart, yStart, xEnd, yEnd):
        # Overwrite default values
        self.SPEED = speed
        self.x_start = xStart
        self.y_start = yStart
        self.x_goal = xEnd
        self.y_goal = yEnd

        self.readFieldData()
        self.isStartOrGoalPositionAWall()
        self.buildBFSWalls()
        self.initialize()

    # Initialize pygame, set window title, set window height/width
    def initialize(self):
        pg.init()
        self.WINDOW = pg.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption(self.WINDOW_TITLE)
        counter = 0

        while self.isGameActive:
            for event in pg.event.get():
                # Set isGameActive to False because user pressed quit
                if event.type == pg.QUIT:
                    self.isGameActive = False
            # check if the things are already drawn (prevents flackyness)
            if counter == 0:
                # Set background color
                self.WINDOW.fill(self.BLACK)
                # draw goal position
                self.drawCircle(self.x_goal, self.y_goal, self.WHITE)
                # draw start position
                self.drawCircle(self.x_start, self.y_start, self.GREEN)
                # draw walls
                self.drawWalls()
                pg.display.update()
                self.makeSteps()
                counter += 1

    # Read file for building the maze
    def readFieldData(self):
        # read file in text mode
        with open("field.txt", 'rt') as file:
            # X dimension of field
            x_dimension = int(file.readline())
            self.X_FIELD_DIMENSION = x_dimension
            # set window width, which dependents on X dimension ( + 1 for extra space)
            self.WINDOW_WIDTH = (x_dimension + 1) * self.BLOCK_SIZE
            # Y dimension of field
            y_dimension = int(file.readline())
            self.Y_FIELD_DIMENSION = y_dimension
            # set window height, which dependents on Y dimension ( + 1 for extra space)
            self.WINDOW_HEIGHT = (y_dimension + 1) * self.BLOCK_SIZE

            # checking if the given values for the field dimensions are valid, closing if not
            if self.areDimensionsValid() == False:
                exit()

            # read rows and create always a new array until \n (line breaks) come in
            rows = file.read().splitlines()
            cols = []
            for line in rows:
                # splitlines() creates string arrays e.g. ['0', '1', ...]
                # convert array values from type string to int e.g. [0, 1, ...]
                lineToInt = list(map(int, line.split()))
                cols.append(lineToInt)
            self.WALLS = cols

    # Draw all walls
    def drawWalls(self):
        for row, rowValue in enumerate(self.WALLS):
            for col, colValue in enumerate(rowValue):
                # check for walls which are 1s
                if colValue == 1:
                    xPosStart = col * self.BLOCK_SIZE
                    xPosEnd = xPosStart + self.BLOCK_SIZE
                    yPos = row * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
                    self.drawWall(xPosStart, yPos, xPosEnd)
        pg.display.update()

    # Draw wall
    def drawWall(self, x_start, y_current, x_end):
        pg.draw.line(self.WINDOW, self.BLUE, (x_start, y_current),
                     (x_end, y_current), self.BLOCK_SIZE)

    # Draw circle at given x, y coordinates and color
    def drawCircle(self, x, y, color):
        x_coordinate = x * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
        y_coordinate = y * self.BLOCK_SIZE + self.BLOCK_MIDDLE_SIZE
        pg.draw.circle(self.WINDOW, color, (x_coordinate,
                                            y_coordinate), 6, 0)

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

    # Create matrix with 0s by size of X_FIELD_DIMENSION * Y_FIELD_DIMENSION
    # Set the start point to 1
    def buildBFSWalls(self):
        walls_with_zeros = [
            [0 for _ in range(self.X_FIELD_DIMENSION)] for _ in range(self.Y_FIELD_DIMENSION)]
        # insert 1 which is our starting point
        walls_with_zeros[self.y_start][self.x_start] = 1
        self.BFS_WALLS = walls_with_zeros

    # Find the shortest path and return it
    def getShortedPath(self):
        BFS_MAZE = self.BFS_WALLS
        row, col = (self.y_goal, self.x_goal)
        counter = BFS_MAZE[row][col]
        the_path = [(row, col)]
        # count until the target is reached (which is 1)
        while counter > 1:
            # up
            if row > 0 and BFS_MAZE[row - 1][col] == counter - 1:
                row, col = row - 1, col
                the_path.append((row, col))
                counter -= 1
            # left
            elif col > 0 and BFS_MAZE[row][col - 1] == counter - 1:
                row, col = row, col - 1
                the_path.append((row, col))
                counter -= 1
            # down
            elif row < len(BFS_MAZE) - 1 and BFS_MAZE[row + 1][col] == counter - 1:
                row, col = row+1, col
                the_path.append((row, col))
                counter -= 1
            # right
            elif col < len(BFS_MAZE[row]) - 1 and BFS_MAZE[row][col + 1] == counter - 1:
                row, col = row, col + 1
                the_path.append((row, col))
                counter -= 1
        return the_path

    # Make step by step until we reach goal x, y coordinates
    def makeSteps(self):
        counter = 0
        while self.BFS_WALLS[self.y_goal][self.x_goal] == 0:
            counter += 1
            self.makeStep(counter)
        self.drawShortestPath()

    # Make a step and increase number in BFS_MAZE
    # BFS_MAZE = matrix filled with 0s and one 1 (start position)
    # ORIGINAL_MAZE = matrix filled with 0s and 1s (0 = space, 1 = wall)
    # compare BFS_MAZE with ORIGINAL_MAZE for same row + col and check if it's 0 (no wall)
    def makeStep(self, counter):
        BFS_MAZE = self.BFS_WALLS
        ORIGINAL_MAZE = self.WALLS
        # iterate over rows
        for row in range(len(BFS_MAZE)):
            # iterate over columns
            for col in range(len(BFS_MAZE[row])):
                if BFS_MAZE[row][col] == counter:
                    # going up (current row - 1, column stays same)
                    if row > 0 and BFS_MAZE[row - 1][col] == 0 and ORIGINAL_MAZE[row - 1][col] == 0:
                        BFS_MAZE[row - 1][col] = counter + 1
                        self.drawCircle(col, row - 1, self.ORANGE)
                    # going left (row stays same, current column - 1)
                    if col > 0 and BFS_MAZE[row][col - 1] == 0 and ORIGINAL_MAZE[row][col - 1] == 0:
                        BFS_MAZE[row][col - 1] = counter + 1
                        self.drawCircle(col - 1, row, self.ORANGE)
                    # going down (current row + 1, column stays same)
                    if row < len(BFS_MAZE) - 1 and BFS_MAZE[row + 1][col] == 0 and ORIGINAL_MAZE[row + 1][col] == 0:
                        BFS_MAZE[row+1][col] = counter + 1
                        self.drawCircle(col, row + 1, self.ORANGE)
                    # going right (row stays same, current column + 1)
                    if col < len(BFS_MAZE[row]) - 1 and BFS_MAZE[row][col + 1] == 0 and ORIGINAL_MAZE[row][col + 1] == 0:
                        BFS_MAZE[row][col+1] = counter + 1
                        self.drawCircle(col + 1, row, self.ORANGE)

                    # draw start circle again with the given color
                    self.drawCircle(self.x_start, self.y_start, self.GREEN)
                    # draw goal circle again with the given color
                    self.drawCircle(self.x_goal, self.y_goal, self.WHITE)
                    pg.display.update()
                    self.clock.tick(self.SPEED)

    # Draw the shortest path
    def drawShortestPath(self):
        shortest_path = self.getShortedPath()
        # iterate through shortest_path arra
        for row in range(1, len(shortest_path) - 1):
            coordinates = shortest_path[row]
            x = coordinates[1]
            y = coordinates[0]
            # draw circle to path coordinates
            self.drawCircle(x, y, self.YELLOW)
            pg.display.flip()
            # set speed to low for better visualization
            self.clock.tick(self.SPEED/5)

    # Checking if given field dimensions are valid
    # Checking for: emptiness, smaller than 10 if format is between 16:9 or 9:16
    def areDimensionsValid(self):
        SIXTEEN_BY_NINE_CONSTANT = 1.78
        X_DEVIDED_BY_Y = self.X_FIELD_DIMENSION/self.Y_FIELD_DIMENSION
        Y_DEVIDED_BY_X = self.Y_FIELD_DIMENSION/self.X_FIELD_DIMENSION
        if (self.X_FIELD_DIMENSION or self.Y_FIELD_DIMENSION) == 0:
            print("WARNING: Your maze dimensions are empty.")
            return False
        elif (self.X_FIELD_DIMENSION < 10 or self.Y_FIELD_DIMENSION < 10):
            print("WARNING: Minimum size is 10 blocks by 10 blocks.").format(
                fDIMENSION_BY_BLOCKS=10 * self.BLOCK_SIZE)
            return False
        elif (X_DEVIDED_BY_Y > SIXTEEN_BY_NINE_CONSTANT or Y_DEVIDED_BY_X > SIXTEEN_BY_NINE_CONSTANT):
            print(
                "WARNING: Smallest possible format for field dimensions are 16:9 or 9:16.")
            return False


# speed, xStart, yStart, xGoal, yGoal
Game = Labyrinth(65, 1, 1, 2, 22)
