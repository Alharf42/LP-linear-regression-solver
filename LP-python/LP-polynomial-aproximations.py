import pulp as pl
import math
#the problem
linear = pl.LpProblem("Linear approximation", pl.LpMaximize)

#the constants
point1 = (0, 2)
point2 = (1, 9)
point3 = (2, 2)
point4 = (3, 7)
point5 = (4, 14)
point6 = (5, 16)
point7 = (6, 32)
point8 = (7, 21)
point9 = (8, 13)
point10 = (9, 5) 

points = [(0, 2), (1, 9), (2, 2), (3, 7), (4, 14), (5, 16), (6, 32), (7, 21), (8, 13), (9, 5)]

polynomial_degree = 1
number_of_points = 10

#the variables

distance_delta = pl.LpVariable("distance_delta", lowBound=0)
coefs = []
for i in range(polynomial_degree+1):
    x = pl.LpVariable("x"+str(i))
    coefs.append(x)

#target function
linear += distance_delta

#constraints

sums=[]

for point in points:
    sum =0
    for j in range(polynomial_degree+1):
        sum += coefs[j]*math.pow(point[0],j)
    sums.append(sum)    

#equations constraints
for i in range(number_of_points):
    linear += sums[i] + distance_delta <= points[i][1]
    linear += sums[i] - distance_delta >= points[i][1]

#nonnegative constraints
# for coef in coefs:
#     linear += coef >= 0
#linear += distance_delta >=0

for sum in sums:
    print(str(sum))

for i in range(number_of_points):
    print(str(sums[i]) +" + "+ str(distance_delta) +" <= " + str(points[i][1]))
    print(str(sums[i]) +" - "+ str(distance_delta) +" >= " + str(points[i][1]))

#solution
solution = linear.solve()

print(f"SOLUTION")
for i in range(polynomial_degree+1):
    print("x"+str(i)+f" = {pl.value(coefs[i])}")
print(f"Maximum of minimal distances: {pl.value(linear.objective)}")
optimum = pl.value(linear.objective)
cfs =[pl.value(coef) for coef in coefs]

import matplotlib.pyplot as plt
import numpy as np

arrayX=[]
for point in points:
    arrayX.append(point[0])
x= np.array(arrayX)

arrayY=[]
for point in points:
    arrayY.append(point[1])
y= np.array(arrayY)

def f(x):
    return sum(cfs[i]*x**i +optimum for i in range(len(cfs)))

t = np.linspace(0,10,100)
#polynomial_values = [f(val) for val in t]

plt.plot(t,f(x))
plt.scatter(x,y)
plt.show()