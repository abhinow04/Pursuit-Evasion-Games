import numpy as np
import assign
N = 2 #Dimension of motion (2D)
m = 2 #Number of pursuers
n = 2 #Number of evaders
v = np.ones(m) #Pursuer speed
u = np.ones(n) #Evader speeds
r = 0.01 #Time Stamp



pur_pos = np.array([[-1.7220,0.3751],[7.7220,0.3751]])
ev_pos = np.array([[9.1501,-6.8477],[3.2978,9.4119]])
target = np.array([0,0])
pur_sp = np.array([[11]] * m)
eva_sp = np.array([[10]] * n)


asgn = assign.assignment(pur_pos,ev_pos,target,v,pur_sp,eva_sp)
asgn.check_win()
asgn.plot_current_positions()
done = False
t = 1
time_chunk = 1000
