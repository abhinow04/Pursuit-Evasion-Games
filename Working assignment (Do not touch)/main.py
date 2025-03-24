import numpy as np
import assign
N = 2 
n = 2 
m = 2 
v = np.ones(m) 
u = np.ones(n) 
r = 1 

pur_pos = 300 * np.random.randn(n,N)
ev_pos = 200 * np.random.randn(m,N)
print("Pursuer position: ",pur_pos)
print("Evader position: ",ev_pos)

target = np.array([0,0])

##pur_sp = 0.1 * np.random.rand(n,1)
##eva_sp = 0.1 * np.random.rand(m,1)
pur_sp = np.array([[30]] * n)
eva_sp = np.array([[25]] * m)

asgn = assign.assignment(pur_pos,ev_pos,target,v,pur_sp,eva_sp)
asgn.check_win()
