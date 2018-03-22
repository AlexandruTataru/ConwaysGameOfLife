from graphics import *
import time
import random
from threading import Thread

GAME_RES_X = 11
GAME_RES_Y = 11

CELL_SIZE = 30

WINDOW_SIZE_X = GAME_RES_X * CELL_SIZE
WINDOW_SIZE_Y = GAME_RES_Y * CELL_SIZE

window = GraphWin("Game Of Life", WINDOW_SIZE_X, WINDOW_SIZE_Y)

COLOR_CELL_ALIVE = color_rgb(255, 255, 255)
COLOR_CELL_DEAD = color_rgb(0, 0, 0)

STATE_CELL_ALIVE = 1
STATE_CELL_DEAD = 0

uiCells = []

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = STATE_CELL_DEAD
        self.prev_state = STATE_CELL_DEAD;
        p1 = Point(x, y)
        p2 = Point(x + CELL_SIZE, y)
        p3 = Point(x + CELL_SIZE, y + CELL_SIZE)
        p4 = Point(x, y + CELL_SIZE)
        vertices = [p1, p2, p3, p4]
        self.shape = Polygon(vertices)

        self.shape.setFill(COLOR_CELL_DEAD)

    def SetState(self, newState):
        self.prev_state = self.state
        self.state = newState

    def GetState(self):
        return self.state

    def Draw(self):
        self.shape.draw(window)

    def ReDraw(self):
        if self.state == self.prev_state:
            return
        
        if self.state == STATE_CELL_DEAD:
            self.shape.setFill(COLOR_CELL_DEAD)
        else:
            self.shape.setFill(COLOR_CELL_ALIVE)

def drawBoard():
    global uiCells
    startX = 0
    startY = 0
    for hor in range(0, GAME_RES_Y):
        for ver in range(0, GAME_RES_X):
            cell = Cell(startX, startY)
            cell.Draw()
            uiCells.append(cell)
            startX = startX + CELL_SIZE
        startX = 0
        startY = startY + CELL_SIZE

def liniarToPos(liniarValue):
    ver = liniarValue / GAME_RES_X
    hor = liniarValue % GAME_RES_X
    return [hor, ver]

def posToLiniar(x, y):

    if x < 0:
        x = 0
    if y < 0:
        y = 0

    if x >= GAME_RES_Y:
        x = GAME_RES_Y - 1

    if y >= GAME_RES_X:
        y = GAME_RES_X - 1
    
    return y * GAME_RES_X + x;

def getNeighborState(hor, vert):
    global uiCells
    newHor = hor
    newVert = vert

    if hor < 0:
        return 0
    if hor == GAME_RES_X:
        return 0

    if vert < 0:
        return 0
    if vert == GAME_RES_Y:
        return 0

    return uiCells[posToLiniar(newHor, newVert)].GetState()

def getNrNeighbors(hor, vert):
    global uiCells
    aliveNeighbors = 0
    aliveNeighbors = aliveNeighbors + getNeighborState(hor - 1, vert - 1)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor, vert - 1)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor + 1, vert - 1)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor - 1, vert)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor + 1, vert)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor - 1, vert + 1)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor, vert + 1)
    aliveNeighbors = aliveNeighbors + getNeighborState(hor + 1, vert + 1)

    return aliveNeighbors

def updateCellsInternalValue():
    global uiCells
    values = []
    counter = 0
    for cell in uiCells:
        hor, vert = liniarToPos(counter)
        aliveNeighbors = getNrNeighbors(hor, vert)
        if cell.GetState() == STATE_CELL_ALIVE:
            if aliveNeighbors < 2:
                values.append(0)
            elif aliveNeighbors == 2 or aliveNeighbors == 3:
                values.append(1)
            elif aliveNeighbors > 3:
                values.append(0)
        elif aliveNeighbors == 3:
            values.append(1)
        else:
            values.append(0)       
        
        counter = counter + 1

    c = 0
    for cell in uiCells:
        cell.SetState(values[c])
        c = c + 1

def updateUICells():
    for cell in uiCells:
        cell.ReDraw()
 
def randomizeBoard():
    global uiCells
    for cell in uiCells:
        cell.SetState(STATE_CELL_DEAD)
    #for steps in range(0, 30):
    #    uiCells[random.randint(0, GAME_RES_X * GAME_RES_Y - 1)].SetState(STATE_CELL_ALIVE)
    uiCells[posToLiniar(5, 4)].SetState(STATE_CELL_ALIVE)
    uiCells[posToLiniar(4, 5)].SetState(STATE_CELL_ALIVE)
    uiCells[posToLiniar(5, 5)].SetState(STATE_CELL_ALIVE)
    uiCells[posToLiniar(6, 5)].SetState(STATE_CELL_ALIVE)
    uiCells[posToLiniar(5, 6)].SetState(STATE_CELL_ALIVE)

def threaded_function():
    drawBoard()
    randomizeBoard()
    updateUICells()
    time.sleep(1)
    while True:
        updateCellsInternalValue()
        updateUICells()
        time.sleep(1)

if __name__ == "__main__":
    thread = Thread(target = threaded_function, args = ( ))
    thread.start()
    window.mainloop()
