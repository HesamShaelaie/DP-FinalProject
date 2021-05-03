import math

x = (1,2)
y = (2,2)


def disV1(x,y):
    A = (x[0]-y[0])^2
    B = (x[1]-y[1])^2
    C = math.sqrt*(B+A)
    return C

def disV2(x,y):
    A = abs(x[0]-y[0])
    B = abs(x[1]-y[1])
    C = (B+A)
    return C

class DoSth:
    def __init__(self, x, y, Fun):
        self.x = x
        self.y = y
        self.fun = Fun

    def cal(self):
        self.c = self.fun(self.x,self.y)

    def report(self):
        return self.c


C = DoSth(x,y,disV2)
C.cal()

print(C.report())



