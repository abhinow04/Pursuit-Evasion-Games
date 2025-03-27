import numpy as np
import assign
N = 2 
n = 2 
m = 2 
v = np.ones(m) 
u = np.ones(n) 
r = 1 

pur_pos = [[-50,50],[56,-34]]
ev_pos = [[-53,-23],[34,60]]
print("Pursuer position: ",pur_pos)
print("Evader position: ",ev_pos)

target = np.array([0,0])

##pur_sp = 25 * np.random.rand(n,1)
##eva_sp = 20 * np.random.rand(m,1)
pur_sp = np.array([[30]] * n)
eva_sp = np.array([[17]] * m)

asgn = assign.assignment(pur_pos,ev_pos,target,v,pur_sp,eva_sp)

x=int(input())
asgn.check_win()
print(asgn.cap_point)
