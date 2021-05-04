import numpy as np
import random
x = np.zeros((2,3,4))
x[1,2,3] = 1
#print(x[1,2,3])

#print(x[1,1,3])
B = [1,1,3]
C = (B)
#print(*C)
#print(x[B])
#print(x[B[0],B[1],B[2]])
#print(x[(B[i] for i in range(3))])
#print(x[(1,1,3)])
print(x[tuple(B)])
#dims = tuple([random.randint(1,100) for _ in range(10)])
#print(dims)
