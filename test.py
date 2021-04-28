import numpy as np

y = np.array([1, 2, 3])
print(y)

dt = np.dtype([('name', np.unicode_, 16), ('grades', np.float64, (2,))])
x = np.array([('Sarah', (8.0, 7.0)), ('John', (6.0, 7.0))], dtype=dt)
print(x[1])
print(x[1]['grades'])
print(x[1][1])


x[1][1][0] = 3000
print(x[1][1])




 