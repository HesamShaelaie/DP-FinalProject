def initializeGrid(cellRows, cellColumns):

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
    for y in range (cellColumns):
        for x in range (cellRows):
            initialdict[(x,y)] = [[0,1,1,1],[1,1,1,1]]

    #constraints
    
    
    return initialdict


A = initializeGrid(10,10)

print(A[(1,2)])
print(A[(1,2)][0])
