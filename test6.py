A= [1,2,3,4,5]

B = A[:-1]

C= tuple(B)
print(A)
print(B)
print(C)
A[0] = 20

print(A)
print(B)
print(C)

B[0]=30
print(A)
print(B)
print(C)


A = [1,2,3,4,5]

B = {}

B[(1,2)] = A 

print(B[(1,2)])