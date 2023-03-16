import numpy as np
A = np.array([[1, 0, 0],
[0, 0.5, -0.5],
[0, 0.5, 0.5]])
C = np.array([[ 0.9998361,  -0.00860898  ,0.0159264 ],
 [-0.00959822 , 0.49383421 , 0.8695031 ],
 [-0.01535053 ,-0.86951346 , 0.49367064]])
# Find the inverse of A
A_inv = np.linalg.inv(A)

# Compute matrix B
B = np.dot(A_inv, C)

print(B)