from scipy.optimize import minimize

f = lambda x:  x**2
x0 = [-2]
cost = minimize(f,x0)

print(cost.x[0])
