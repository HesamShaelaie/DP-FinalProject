
import pygame, random, sys, numpy as np
# from time import time

     
def initializeGrid(cellRows, cellColumns):

    #create empty dictionary
    initialdict = {}
    #for each cell on the grid (with key x,y) set it to 0 (dead)
    for y in range (cellColumns):
        for x in range (cellRows):
            #generate a number from 0 to 100
            num = np.random.randint(0,101)
            # if the number is 0 to 25 (which should randomly be around 25% of the grid)
            if num <= 25:
                initialdict[(x,y)] = 1    #25% of cells will be alive (1)
            else:
                initialdict[(x,y)] = 0    #75% of cells will be dead (0)
        
    return initialdict


def drawGridLines(screen, width, height, cellsize):
   
    #from 0 to 600 (or whatever screen width) increasing by the length of a cell
    for x in range(0, width, cellsize):
        #draw a line from the top of the screen (0) to the bottom (height) going to the right by  x
        pygame.draw.line(screen, (50, 50, 50), (x,0),(x,height)) # draw vertical lines
    
    #from 0 to 600 (or whatever screen height)
    for y in range (0, height, cellsize): 
        #draw a line from the left of the screen (0) to right (width) going down by y
        pygame.draw.line(screen, (50, 50, 50), (0,y), (width, y)) # draw horizontal lines


def colorCell(key, celldict, cellsize, screen):
    """     
     colorCell colors an individual cell in the dictionary of cells based on whether it is
     alive (orange) or dead( black)
     
     
     Parameters
     ----------
     key: tuple 
         the key is the pair of coordinates (x,y) to a single cell in the dictionary
     celldict: dictionary
         the dictionary of all of the cells on the grid
     cellsize: int
         the size of a side of each cell (which is a square)
     screen: pygame.Surface
         the surface that we draw on using pygame
     
     Returns
     -------
         Nothing
    """
    x = key[0]    #take first element of key from celldict (x coordinate)
    y = key[1]    #take second element (y coordinate)
    x = x * cellsize  # change x and y into grid-size coordinates
    y = y * cellsize 
    if celldict[key] == 0:  #if the value at that key is 0 (dead)
        pygame.draw.rect(screen, (0, 0, 0), (x, y, cellsize, cellsize))  #draw black square
    elif celldict[key] == 1:   #if value at that key is 1 (alive)
        pygame.draw.rect(screen, (255, 140, 0), (x, y, cellsize, cellsize)) #draw orange square
        #pygame.draw.rect(screen, color, (xpos, ypos, width, height))


#Count how many alive neighbors are around each cell
def countNeighbors(key, celldict, cellRows, cellColumns):
    """     
     countNeighbors counts the number of alive neighbors surrounding a single cell
     
     
     Parameters
     ----------
     key: tuple 
         the key is the pair of coordinates (x,y) to a single cell in the dictionary (each cell is colored
         in a for loop in the main)
     celldict: dictionary
         the dictionary of all of the cells on the grid
     cellRows: int
         the number of cells in each row of the grid (the number of cells wide) found by dividing width of screen by cellsize
     cellColumns: int 
         the number of cells in each column of the grid (the number of cells high) found by dividing height of screen by cellsize
     
     Returns
     -------
     neighbors: int
         the number of living cells surrounding the current cell (at the key)
    """
    neighbors = 0
    for x in range (-1,2):    #checks -1, 0, 1
        for y in range (-1,2):
            #checkCell variable checks all combinations of cells around the cell[key] that was passed to the method
            #checks (xpos-1, ypos-1), (xpos-1, ypos+0), (xpos-1, ypos+1)
            #(xpos+0, ypos-1), (xpos, ypos) <-- which we don't consider b/c it's the cell we're checking around
            #(xpos, ypos+1), (xpos+1, ypos-1), (xpos+1, ypos), (xpos+1, ypos+1)
            checkCell = (key[0]+x, key[1]+y)  
            if checkCell[0] < cellRows  and checkCell[0] >=0 and checkCell[1] < cellColumns and checkCell[1]>= 0:  #if position is on grid
                if celldict[checkCell] == 1:     #if the cell at the position being checked around the center cell is alive
                    if x == 0 and y == 0: #leave out the center cell
                        neighbors += 0
                    else:
                        neighbors += 1   #increment the alive neighbor (as long as it's not the center cell)
    return neighbors


#Determine the next generation of cells
def nextStep(celldict, cellRows, cellColumns):
    """     
     nextStep creates a new dictionary that represents the next step or the next generation
     of cells based on the previous one and the number of surrounding living neighbors.
     
     
     Parameters
     ----------
     celldict: dictionary
         the dictionary of all of the cells on the grid
     cellRows: int
         the number of cells in each row of the grid (the number of cells wide) found by dividing width of screen by cellsize
     cellColumns: int 
         the number of cells in each column of the grid (the number of cells high) found by dividing height of screen by cellsize
     
     Returns
     -------
     newGen: dictionary
         a dictionary of the next generation of living and dead cells
    """
    newGen = {}
    for key in celldict:
        #get number of neighbors for each cell
        numberofNeighbors = countNeighbors(key, celldict, cellRows, cellColumns)
        
        # If the cell is currently alive
        if celldict[key] == 1: 
            if numberofNeighbors < 2: # cells with fewer than 2 neighbors die due to under-population
                newGen[key] = 0     # set newly dead cell to 0
            elif numberofNeighbors > 3: # cells with more than three neighbors die from overcrowding
                newGen[key] = 0       # set newly dead cell to 0
            else:                # if the cell has 2 or 3 neighbors it lives to the next generation
                newGen[key] = 1  # cell stays alive (1) into the next generation
        
        # If the cell is currently dead
        elif celldict[key] == 0: 
            if numberofNeighbors == 3: # any dead cell with exactly three neighbors becomes live
                newGen[key] = 1      # set cell to be alive in the next generation
            else:
                newGen[key] = 0      #otherwise, cell stays dead
                
    return newGen


    
def main():
    """     
     main() initializes pygame, initializes the grid of cells, colors, each cell, draws grid lines
     and steps to the next generation continuously in a while loop with a frame rate of 10 FPS.
    """
    FRAMERATE = 10    #frames per second
    
    
    Height = 600
    Width = Height

    CellSizeH = 10
    CellSizeW = 10
    GirdSizeR = 30      #number of rows
    GirdSizeC = 30      #number of columns
    
    CellSizeW = int( Width/GirdSizeC)       # Width of  each cell
    CellSizeH = int( height/GirdSizeR )     # Height of each cell
    
    ClB = (0, 0, 0)                  #color black
    ClW = (255, 255, 255)            #color white
    ClDg = (50, 50, 50)              #color Dark gray
    ClR = (250, 0, 0)                #color red
    CLO = (255, 140, 0)              #color orange
    ClB = (0, 0, 250)                #color blue


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Invader and defender game')
    screen.fill(ClW)
    pygame.display.update()    
    '''
    celldict = initializeGrid(cellRows, cellColumns) 
    
    #initially draw grid lines and the colored rectangle for each cell based on whether it's alive or dead
    for cell in celldict:
        colorCell(cell, celldict, cellsize, screen)
    drawGridLines(screen, width, height, cellsize)
    pygame.display.update()
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    #     screen.fill(black)
    
        # replace cellDict with next generation of cells
        celldict = nextStep(celldict, cellRows, cellColumns)
    
        # re-color the cells to their new status of dead/alive
        for key in celldict:
            colorCell(key, celldict, cellsize, screen)
        drawGridLines(screen, width, height, cellsize)    # re-draw the grid lines
        
        pygame.display.update()    
        clock.tick(FRAMERATE)
    ''''

    
if __name__=='__main__':
    main()

