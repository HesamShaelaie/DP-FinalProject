
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
    def __init__(self, Type, ID, NRow, NClm, Cl, ClBck, R, WC, Width, Height, screen, Moves, XYlist, RcList):
        self.Type = Type
        
        self.x = random.randint(0,NRow-1)
        self.y = random.randint(0,NClm-1)
        self.ID = ID
        self.Cl = Cl
        self.R = R
        self.Rc = int(R*1.1)
        self.WC = WC
        self.ClBck = ClBck
        self.Dirt = random.randint(0,3)
        self.Width = Width
        self.Height = Height
        self.rmStp = 5
        self.Px = (self.x * Width) + int(Width/2)
        self.Py = (self.y * Height) + int(Height/2)
        
        self.NRow = NRow
        self.NClm = NClm
        self.XYlist = XYlist
        self.RcList = RcList

        #self.PRx = (x * Width)
        #self.PRy = (y * Height)
        #self.Rec = pygame.Rect(self.PRx, self.PRy, self.Width, self.Height)

        self.PRx = self.Px - math.ceil(self.Rc/2.0)
        self.PRy = self.Py - math.ceil(self.Rc/2.0)
        self.Rec = pygame.Rect(self.PRx, self.PRy, self.Rc, self.Rc)

        self.screen = screen
        self.Moves = Moves

        Cnt = self.ID*2
        self.XYlist[Cnt] = self.x
        self.XYlist[Cnt+1] = self.y



    def UpPn(self, x, y):

        if x>= self.NRow or x<0:
            print(x)
            print("x input error!!!")
            exit(2)

        if y>= self.NClm or y<0:
            print(y)
            print("x input error!!!")
            exit(2)

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

        Cnt = self.ID*2
        self.XYlist[Cnt] = self.x
        self.XYlist[Cnt+1] = self.y


    def RnIndx(self):
        return self.x, self.y

    def RnPR(self):
        return self.PRx, self.PRy, self.Width, self.Height


    def DrawBALL(self):
        pygame.draw.circle(self.screen, self.Cl, (self.Px,self.Py), self.WC, self.R)
        Cnt = self.ID*2
        self.RcList[Cnt] = self.Rec

    def RemoveBALL(self):
        pygame.draw.rect(self.screen, self.ClBck, self.Rec)
        Cnt = self.ID*2
        self.RcList[Cnt + 1] = self.Rec

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
            #print(self.rmStp)


        if t==0:
            self.UpPn((self.x),(self.y-1))
        elif t==1:
            self.UpPn((self.x),(self.y+1))
        elif t==2:
            self.UpPn((self.x-1),(self.y))
        else:
            self.UpPn((self.x+1),(self.y))

    def QL_Par(self, Gamma, Epz, NInv, NDef):

        self.Gamma = Gamma
        self.Epz = Epz
        self.NDef = NDef
        self.NInv = NInv
        

    def QL_Up_Epz(self, Epz):
        self.Epz = Epz

    def QL_Env(self):
        Dim = []
        for _ in range(self.NInv):
            Dim.append(self.NRow)
            Dim.append(self.NClm)

        for _ in range(self.NDef):
            Dim.append(self.NRow)
            Dim.append(self.NClm)

        self.V = np.zeros(tuple(Dim))
        Dim.append(4)
        self.Q = np.zeros(tuple(Dim))
    



class Balls_Info():
    def Init_Screen(self, screen, Hsc, Wsc, ClBack):
        self.Scr = screen
        self.ScrH = Hsc
        self.ScrW = Wsc
        self.ClBack = ClBack

    def Init_Env(self, NRow, NClm, CellW, CellH):
        self.NRow = NRow
        self.NClm = NClm
        self.CellW = CellW
        self.CellH = CellH

    def Init_Inv(self, NInv, Cl, R, W, InvMoves):
        self.InvN = NInv
        self.InvCl = Cl
        self.InvR = R
        self.InvW = W
        self.InvMoves = InvMoves

    def Init_Def(self, NDef, Cl, R, W, DefMoves):
        self.DefN = NDef
        self.DefCl = Cl
        self.DefR = R
        self.DefW = W
        self.DefMoves = DefMoves

    def Init_QLn(self, Gamma, Epz, InvChaM, StepSize):
        self.Gamma = Gamma
        self.Epz = Epz
        self.InvChaM = InvChaM
        self.StepSize = StepSize
        

    def Create(self):
        Cnt = 0
        
        self.Total = self.InvN + self.DefN
        self.RecList = [pygame.Rect(0,0,10,10)]*(2*self.Total)
        self.XYlist = [0]*(self.Total*2)
        self.XYlist.append(0)

        self.InvList = []
        for _ in range(self.InvN):
            self.InvList.append(BALL(True, Cnt, self.NRow, self.NClm, self.InvCl, self.ClBack, self.InvR, self.InvW, self.CellW, self.CellH, self.Scr , self.InvMoves, self.XYlist, self.RecList))
            Cnt += 1

        self.DefList = []
        for _ in range(self.DefN):
            self.DefList.append(BALL(False, Cnt, self.NRow, self.NClm, self.DefCl, self.ClBack, self.DefR, self.DefW, self.CellW, self.CellH, self.Scr , self.DefMoves, self.XYlist, self.RecList))
            Cnt += 1
        
        for x in self.InvList:
            x.QL_Par(self.Gamma, self.Epz, self.InvN, self.DefN)
            x.QL_Env()
        
        for y in self.DefList:
            y.QL_Par(self.Gamma, self.Epz, self.InvN, self.DefN)
            y.QL_Env()



    def Init_Position(self):
        Plist = []
        
        for x in self.InvList:
            while True:
                R = random.randint(0, self.NRow-1)
                C = random.randint(0, self.NClm-1)
                if (R,C) not in Plist:
                    Plist.append((R,C))
                    x.UpPn(R,C)
                    break
        
        for y in self.DefList:
            while True:
                R = random.randint(0, self.NRow-1)
                C = random.randint(0, self.NClm-1)
                if (R,C) not in Plist:
                    Plist.append((R,C))
                    y.UpPn(R,C)
                    break


    
    def Draw(self):
        
        for x in self.InvList:
            x.DrawBALL()
            
        for y in self.DefList:
            y.DrawBALL()
            

    def Remove(self):

        for x in self.InvList:
            x.RemoveBALL()
            
        for y in self.DefList:
            y.RemoveBALL()
            

    def Move(self):
        
        for x in self.InvList:
            x.MoveDirtv2(5)
            
        for y in self.DefList:
            y.MoveDirtv2(5)

    def UpdateScreen(self, Key):
        
        #Key=0 -> both remove and draw
        #Key=1 -> only draw
        #Key=2 -> only remove

        if Key == 0:
            pygame.display.update(self.RecList)
        elif Key ==1:
            pygame.display.update(self.RecList[0:self.Total])
        else:
            pygame.display.update(self.RecList[self.Total:])
    
    def QLmove(self):

        for Inv in self.InvList:
            
            RND = random.random()
            Act = 0
            
            x = Inv.x
            y = Inv.y
            T = self.Total

            Dumy = 0

            if RND < self.Epz:

                while True:
                    Act = random.randint(0,3)
                    Dumy += 1
                    if Inv.Moves[(x,y)][Act]:
                        break

                    if  Dumy>30:
                        print("Cannot find an action to pick in epz!!!")
                        exit(2)


            else:

                MaxVl = -1000000
                MaxIn = -1
                TmpVl = 0.0
                Fkey = False
                Indx = random.randint(0,3)

                for _ in range(3):

                    if Inv.Moves[(x,y)][Indx]:
                        self.XYlist[T] = Indx
                        IndxMx = tuple(self.XYlist)
                        TmpVl = Inv.Q[IndxMx]
                        if MaxVl < TmpVl:
                            MaxVl = TmpVl
                            MaxIn = Indx
                            Fkey = True
                    Indx += 1
                    if Indx == 4:
                        Indx=0
                
                if not Fkey:
                    print("Cannot find an action to pick in non epz!!!")
                    exit(2)

                Act = MaxIn

            self.XYlist[T] = Act

            IndxMxQ = tuple(self.XYlist)
            IndxPrV = tuple(self.XYlist[:-1])
    
            #check termination
            if Act == 0:
                Inv.UpPn((Inv.x),(Inv.y-1))
                y = y-1
            elif Act == 1:
                Inv.UpPn((Inv.x),(Inv.y+1))
                y = y+1
            elif Act == 2:
                Inv.UpPn((Inv.x-1),(Inv.y))
                x = x-1
            else:
                Inv.UpPn((Inv.x+1),(Inv.y))
                x = x+1

            IndxNtV = tuple(self.XYlist[:-1])

            Catch = False
            for Def in self.DefList:
                if Def.x == x and Def.y==y:
                    Catch = True
                    break

            
            # rewards
            ImdReward = 0.0

            if Catch:
                ImdReward = -1.0
            else:
                ImdReward = 0.0


            Inv.Q[IndxMxQ] = Inv.Q[IndxMxQ] + self.StepSize*(ImdReward +  (self.Gamma*(Inv.V[IndxNtV])) - Inv.Q[IndxMxQ])
            if Inv.V[IndxPrV] < Inv.Q[IndxMxQ]:
                Inv.V[IndxPrV] = Inv.Q[IndxMxQ]

            if Catch:
                return True
            
        for Def in self.DefList:
            
            Act = 0
            x = Def.x
            y = Def.y
            T = self.Total

            MinVl = +1000000
            MinIn = -1
            TmpVl = 0.0
            Fkey = False
            Indx = random.randint(0,3)

            for _ in range(3):
                
                if Def.Moves[(x,y)][Indx]:
                    self.XYlist[T] = Indx
                    IndxMx = tuple(self.XYlist)
                    TmpVl = Def.Q[IndxMx]
                    if MinVl > TmpVl:
                        MinVl = TmpVl
                        MinIn = Indx
                        Fkey = True
                Indx += 1
                if Indx == 4:
                    Indx=0
            
            if not Fkey:
                print("Cannot find an action to pick in non epz!!!")
                exit(2)

            Act = MinIn

            self.XYlist[T] = Act

            IndxMxQ = tuple(self.XYlist)
            IndxPrV = tuple(self.XYlist[:-1])
    
            #check termination
            if Act == 0:
                Def.UpPn((Def.x),(Def.y-1))
                y = y-1
            elif Act == 1:
                Def.UpPn((Def.x),(Def.y+1))
                y = y+1
            elif Act == 2:
                Def.UpPn((Def.x-1),(Def.y))
                x = x-1
            else:
                Def.UpPn((Def.x+1),(Def.y))
                x = x+1

            IndxNtV = tuple(self.XYlist[:-1])

            Catch = False
            for Inv in self.InvList:
                if Inv.x == x and Inv.y==y:
                    Catch = True
                    break

            
            # rewards
            ImdReward = 0.0

            if Catch:
                ImdReward = -1.0
            else:
                ImdReward = 0.0

            Def.Q[IndxMxQ] = Def.Q[IndxMxQ] + self.StepSize*(ImdReward +  (self.Gamma*(Inv.V[IndxNtV])) - Def.Q[IndxMxQ])
            if Def.V[IndxPrV] > Def.Q[IndxMxQ]:
                Def.V[IndxPrV] = Def.Q[IndxMxQ]

            if Catch:
                return True

        return False    




def main():
    
    """     
     main() initializes pygame, initializes the grid of cells, colors, each cell, draws grid lines
     and steps to the next generation continuously in a while loop with a frame rate of 10 FPS.
    """

    Height = 600
    Width = Height

    
    NRow = 15      #number of rows
    NClm = NRow      #number of columns
    
    CellSizeW = int( Width/NClm)       # Width of  each cell
    CellSizeH = int( Height/NRow )     # Height of each cell
    CellsDic, InvMoves, DefMoves = initializeGrid(NRow, NClm, CellSizeH, CellSizeW)
    

    # ============ Q learning paramters =============================
    
    NDef = 2
    NInv = 1
    Gamma = 0.5
    Epz = 0.1
    InvChaM = 0.9 # chance of moving invader at each event
    StepSize = 0.3

    #======================   Colors dictionary =====================
    ClBk = (0, 0, 0)                  #color black
    ClWt = (255, 255, 255)            #color white
    ClDg = (50, 50, 50)              #color Dark gray
    ClRd = (250, 0, 0)                #color red
    CLOr = (255, 140, 0)              #color orange
    ClBl = (0, 0, 250)                #color blue
    #======================   Colors dictionary =====================
    
    pygame.init()
    clock = pygame.time.Clock()
    #print(CellsDic[(5,5)])
    screen = pygame.display.set_mode((Width,Height))
    pygame.display.set_caption('Invader and Defender Game')

    screen.fill(ClWt)
    drawGridLines(screen, ClBk, Width, Height, CellSizeW, CellSizeH)
    drawConstraints(screen, CellsDic, NRow, NClm, CellSizeH, CellSizeW, 10)
    
    pygame.display.update() 
    
    #=====================    creating balls  =======================
    R = min(CellSizeH,CellSizeW)
    R = int(R*0.5)

    Balls = Balls_Info()
    Balls.Init_Screen(screen, Width, Height, ClWt)
    Balls.Init_Env(NRow, NClm, CellSizeW, CellSizeH)
    Balls.Init_Inv(NInv, ClRd, R, 8, InvMoves)
    Balls.Init_Def(NDef, ClBl, R, 8, DefMoves)
    Balls.Init_QLn(Gamma, Epz, InvChaM, StepSize)
    Balls.Create()

    #=====================    creating balls  =======================
    
    FRAMERATE = 10
    clock.tick(FRAMERATE)
    
    AveLimit = 200
    AveEpd = 0.0
    CntEpd = 0      #Count episode
    CntEnt = 0      #Count event in one episode
    CntListEpd = np.zeros(AveLimit)

    font = pygame.font.Font('freesansbold.ttf', 16)
    text1 = font.render('Epz:   ' + str(CntEpd), True, ClWt, ClBl)
    textRect1 = text1.get_rect()
    textRect1.center = (50, 20)

    text2 = font.render('Ave:   ' + str(AveEpd), True,  ClWt, ClBl)
    textRect2 = text1.get_rect()
    textRect2.center = (50, 40)

    text3 = font.render('Evn:   ' + str(CntEnt), True,  ClWt, ClBl)
    textRect3 = text3.get_rect()
    textRect3.center = (50, 60)
 
# infinite loop

    Terminate = False
    Balls.Init_Position()
    Balls.Draw()
    Balls.UpdateScreen(1)

    while True: 
        
        text1 = font.render('Epz:   ' + str(CntEpd), True, ClWt, ClBl)
        text2 = font.render('Ave:   ' + str(AveEpd), True,  ClWt, ClBl)
        text3 = font.render('Evn:   ' + str(CntEnt), True,  ClWt, ClBl)

        screen.blit(text1, textRect1)
        screen.blit(text3, textRect3)
        screen.blit(text2, textRect2)
        pygame.display.update([textRect1,textRect2,textRect3])

        Balls.Remove()
        #Balls.Move()
        Terminate = Balls.QLmove()
        #print(Balls.InvList[0].Q(tuple([1,1, 1,1, 1,1, 1,1, 1])))
        #print(Balls.InvList[0].Q[1,1, 1,1, 1,1, 1,1, 1])
        Balls.Draw()
        Balls.UpdateScreen(0)

        if Terminate:

            Balls.Remove()
            Balls.Init_Position()
            Balls.Draw()
            Balls.UpdateScreen(0)

            Indx = CntEpd % AveLimit
            CntListEpd[Indx] = CntEnt

            CntEnt = 0 
            CntEpd += 1

            if CntEpd > AveLimit:
                AveEpd = np.mean(CntListEpd)
            else:
                AveEpd = np.mean(CntListEpd[0:CntEpd])
        else:
            CntEnt += 1

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        clock.tick(FRAMERATE)

    
if __name__=='__main__':
    main()

