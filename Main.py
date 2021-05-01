
import pygame, sys, numpy as np
import random 
import math
# from time import time

     
def initializeGrid(NRows, NColumns,H,W):

    '''
    dt = np.dtype([
                    ('I', np.uint8),
                    ('J', np.uint8),
                    ('IB', np.bool, (4,))
                    ('AB', np.bool, (4,))
                    ])

    '''
    
    #lines(surface, color, closed, points, width=1)
    
    
    initialdict = {}
    for y in range (NColumns):
        for x in range (NRows):
            initialdict[(x,y)] = [[x*W,y*H],[1,1,1,1],[1,1,1,1]] #U D L R

    for x in range (NColumns):

        initialdict[(x,0)][1] = [0,1,1,1]
        initialdict[(x,0)][2] = [0,1,1,1]

        initialdict[(x,NRows-1)][1] = [1,0,1,1]
        initialdict[(x,NRows-1)][2] = [1,0,1,1]
        
    for y in range (NRows):
        initialdict[(0,y)][1] = [1,1,0,1]
        initialdict[(0,y)][2] = [1,1,0,1]

        initialdict[(NColumns-1,y)][1] = [1,1,1,0]
        initialdict[(NColumns-1,y)][2] = [1,1,1,0]
    
    initialdict[(0,0)][1] = [0,1,0,1]
    initialdict[(0,0)][2] = [0,1,0,1]

    initialdict[(0,NRows-1)][1] = [1,0,0,1]
    initialdict[(0,NRows-1)][2] = [1,0,0,1]

    initialdict[(NColumns-1,0)][1] = [0,1,1,0]
    initialdict[(NColumns-1,0)][2] = [0,1,1,0]

    initialdict[(NColumns-1,NRows-1)][1] = [1,0,1,0]
    initialdict[(NColumns-1,NRows-1)][2] = [1,0,1,0]


    #U D L R: up down left right

    initialdict[(5,5)][2] =  [0,1,1,1]
    initialdict[(6,5)][2] =  [0,1,1,1]
    initialdict[(7,5)][2] =  [0,1,1,0]
    initialdict[(7,6)][2] =  [1,1,1,0]
    initialdict[(7,7)][2] =  [1,1,1,0]
    initialdict[(7,8)][2] =  [1,1,1,0]
    initialdict[(7,9)][2] =  [1,1,1,0]

    #x - go to the right
    #y - go to the down
    # 2 -> defender -> blue
    # 1 -> Invader  -> red
    initialdict[(5,4)][2] =  [1,0,1,1]
    initialdict[(6,4)][2] =  [1,0,1,1]
    initialdict[(7,4)][2] =  [1,0,1,1]
    initialdict[(8,5)][2] =  [1,1,0,1]
    initialdict[(8,6)][2] =  [1,1,0,1]
    initialdict[(8,7)][2] =  [1,1,0,1]
    initialdict[(8,8)][2] =  [1,1,0,1]
    initialdict[(8,9)][2] =  [1,1,0,1] 

    InvMoves = {}
    DefMoves = {}
    for x in range(NRows):
        for y in range(NColumns):
            InvMoves[(x,y)] = initialdict[(x,y)][1]
            DefMoves[(x,y)] = initialdict[(x,y)][2]

    return initialdict , InvMoves, DefMoves


def drawGridLines(screen, Cl, width, height, CellW, CellH):
   
    
    for x in range(0, width, CellW):
        pygame.draw.line(screen, Cl, (x,0),(x,height))
    
    
    for y in range (0, height, CellH): 
        pygame.draw.line(screen, Cl, (0,y), (width, y))

def drawConstraints(screen, CellsDic, NRow, NClm, CellSizeH, CellSizeW, Size):
    ClBk = (0, 0, 0)                  #color black
    ClWt = (255, 255, 255)            #color white
    ClDg = (50, 50, 50)              #color Dark gray
    ClRd = (250, 0, 0)                #color red
    CLOr = (255, 140, 0)              #color orange
    ClBl = (0, 0, 250) 

    Size
    for x in range(NRow):
        for y in range(NClm):
            for z in range(4):
                
                A = CellsDic[(x,y)][1][z]
                B = CellsDic[(x,y)][2][z]

                Key = False
                if A==0 and B==0:
                    Cl = ClDg
                    Key = True
                elif A==0:
                    Cl = ClRd
                    Key = True
                elif B==0:
                    Cl = ClBl
                    Key = True
                
                if Key == True:
                    
                    Xc = CellsDic[(x,y)][0][0]
                    Yc = CellsDic[(x,y)][0][1]
                    if z==0:
                        pygame.draw.line(screen, Cl, (Xc,Yc), (Xc + CellSizeW, Yc),Size)
                    elif z==1:
                        pygame.draw.line(screen, Cl, (Xc,Yc+CellSizeH), (Xc+CellSizeW, Yc+ CellSizeH),Size)
                    elif z==2:
                        pygame.draw.line(screen, Cl, (Xc,Yc), (Xc,Yc+CellSizeH),Size)
                    else :
                        pygame.draw.line(screen, Cl, (Xc+CellSizeW,Yc), (Xc+CellSizeW,Yc+CellSizeH),Size)

class BALL:
    def __init__(self, x, y, Cl, ClBck, R, WC, Width, Height, screen, Moves):
        self.x = x
        self.y = y
        self.Cl = Cl
        self.R = R
        self.Rc = int(R*1.1)
        self.WC = WC
        self.ClBck = ClBck
        self.Dirt = random.randint(0,3)
        self.Width = Width
        self.Height = Height
        self.rmStp = 5
        self.Px = (x * Width) + int(Width/2)
        self.Py = (y * Height) + int(Height/2)

        #self.PRx = (x * Width)
        #self.PRy = (y * Height)
        #self.Rec = pygame.Rect(self.PRx, self.PRy, self.Width, self.Height)

        self.PRx = self.Px - math.ceil(self.Rc/2.0)
        self.PRy = self.Py - math.ceil(self.Rc/2.0)
        self.Rec = pygame.Rect(self.PRx, self.PRy, self.Rc, self.Rc)

        self.screen = screen
        self.Moves = Moves

    def UpPn(self, x, y):
        self.x = x
        self.y = y
        self.Px = (x * self.Width) + int(self.Width/2)
        self.Py = (y * self.Height) + int(self.Height/2)
        
        #self.PRx = (x * self.Width)
        #self.PRy = (y * self.Height)
        #self.Rec = pygame.Rect(self.PRx, self.PRy, self.Width, self.Height)

        self.PRx = self.Px - math.ceil(self.Rc/2.0) 
        self.PRy = self.Py - math.ceil(self.Rc/2.0)

        self.Rec = pygame.Rect(self.PRx, self.PRy, self.Rc, self.Rc)
        


    def RnIndx(self):
        return self.x, self.y

    def RnPosition(self):
        return self.Px, self.Py, self.Cl, self.R, self.WC

    def RnPR(self):
        return self.PRx, self.PRy, self.Width, self.Height


    def DrawBALL(self):
        pygame.draw.circle(self.screen, self.Cl, (self.Px,self.Py), self.WC, self.R)

    def RemoveBALL(self):
        pygame.draw.rect(self.screen, self.ClBck, self.Rec)

    def UpdateRegion(self):
        return self.Rec
    
    def Move(self):

        C = 0

        while(True):
            t = random.randint(0,3)
            if self.Moves[(self.x,self.y)][t]:
                break
            C += 1
            if C>30:
                print("Cannot find any valid moves!!!")
                exit(234)

        if t==0:
            self.UpPn((self.x),(self.y-1))
        elif t==1:
            self.UpPn((self.x),(self.y+1))
        elif t==2:
            self.UpPn((self.x-1),(self.y))
        else:
            self.UpPn((self.x+1),(self.y))
            
    def MoveDirt(self):

        C = 0

        t = self.Dirt
        while(True):
            
            if self.Moves[(self.x,self.y)][t]:
                self.Dirt = t
                break
            t = random.randint(0,3)
            C += 1
            if C>30:
                print("Cannot find any valid moves!!!")
                exit(234)

        if t==0:
            self.UpPn((self.x),(self.y-1))
        elif t==1:
            self.UpPn((self.x),(self.y+1))
        elif t==2:
            self.UpPn((self.x-1),(self.y))
        else:
            self.UpPn((self.x+1),(self.y))

    def MoveDirtv2(self, Stps):

        t = self.Dirt
        if not(self.Moves[(self.x,self.y)][t]) or self.rmStp <= 0:
            C = 0
            while(True):

                t = random.randint(0,3)
                if self.Moves[(self.x,self.y)][t]:
                    self.Dirt = t
                    self.rmStp = Stps
                    break
                C += 1
                if C>30:
                    print("Cannot find any valid moves!!!")
                    exit(234)
        else:
            self.rmStp += -1
            print(self.rmStp)


        if t==0:
            self.UpPn((self.x),(self.y-1))
        elif t==1:
            self.UpPn((self.x),(self.y+1))
        elif t==2:
            self.UpPn((self.x-1),(self.y))
        else:
            self.UpPn((self.x+1),(self.y))
    
    

def main():
    """     
     main() initializes pygame, initializes the grid of cells, colors, each cell, draws grid lines
     and steps to the next generation continuously in a while loop with a frame rate of 10 FPS.
    """
    
    
    
    Height = 600
    Width = Height

    
    NRow = 20      #number of rows
    NClm = NRow      #number of columns
    
    CellSizeW = int( Width/NClm)       # Width of  each cell
    CellSizeH = int( Height/NRow )     # Height of each cell
    
    ClBk = (0, 0, 0)                  #color black
    ClWt = (255, 255, 255)            #color white
    ClDg = (50, 50, 50)              #color Dark gray
    ClRd = (250, 0, 0)                #color red
    CLOr = (255, 140, 0)              #color orange
    ClBl = (0, 0, 250)                #color blue


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Width,Height))
    pygame.display.set_caption('Invader and Defender Game')
    screen.fill(ClWt)
    drawGridLines(screen, ClBk, Width, Height, CellSizeW, CellSizeH)
    CellsDic, InvMoves, DefMoves = initializeGrid(NRow, NClm, CellSizeH, CellSizeW)
    pygame.display.update() 
    #print(CellsDic[(5,5)])
    drawConstraints(screen, CellsDic, NRow, NClm, CellSizeH, CellSizeW,10)
    R = min(CellSizeW,CellSizeH)
    R = int(0.5*R)
    pygame.display.update() 

    Intd = BALL(10, 10, ClRd, ClWt, R, 8, CellSizeW, CellSizeH,screen, InvMoves)
    Defr = BALL(6, 6, ClBl, ClWt, R, 8, CellSizeW, CellSizeH,screen, DefMoves)
    ListPositionBalls = [pygame.Rect(0,0,10,10)]*4

    
    Intd.DrawBALL()
    Defr.DrawBALL()

    ListPositionBalls[0] = Intd.UpdateRegion()
    ListPositionBalls[0] = Defr.UpdateRegion()
    pygame.display.update(ListPositionBalls) 

    #pygame.draw.circle(screen, ClRd, (300,300), 15, 10)
    #pygame.draw.line(screen, ClRd, (100,100),(100,200))
    #pygame.display.update() 


    #pygame.display.update()   


    #for cell in celldict:
    #    colorCell(cell, celldict, CellSizeW, screen)
    FRAMERATE = 10    #frames per second
    #pygame.display.update()
    clock.tick(FRAMERATE)

    while True: 
        

        Intd.RemoveBALL()
        Defr.RemoveBALL()
        ListPositionBalls[0] = Intd.UpdateRegion()
        ListPositionBalls[1] = Defr.UpdateRegion()
        #Intd.Move()
        #Defr.Move()
        #Defr.MoveDirt()
        #Intd.MoveDirt()
        Defr.MoveDirtv2(5)
        Intd.MoveDirtv2(5)
        Intd.DrawBALL()
        Defr.DrawBALL()
        ListPositionBalls[2] = Intd.UpdateRegion()
        ListPositionBalls[3] = Defr.UpdateRegion()

        pygame.display.update(ListPositionBalls) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FRAMERATE)

        
        
    

    '''
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    #     screen.fill(black)
    
        # replace cellDict with next generation of cells
        celldict = nextStep(celldict, GirdSizeR, GirdSizeC)
    
        # re-color the cells to their new status of dead/alive
        for key in celldict:
            colorCell(key, celldict, cellsize, screen)
        drawGridLines(screen, width, height, cellsize)    # re-draw the grid lines
        
        pygame.display.update()    
        
    '''

    
if __name__=='__main__':
    main()

