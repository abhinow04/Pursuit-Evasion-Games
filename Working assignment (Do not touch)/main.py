#Import libraries
import numpy as np
import assign 
N = 2 #Number of dimensions
n = 2 #Number of Pursuers
m = 2 #Number of Evaders 
r = 1 

pur_pos = 300 * np.random.randn(n,N)
ev_pos = 200 * np.random.randn(m,N)
print("Pursuer position: ",pur_pos)
print("Evader position: ",ev_pos)

target = np.array([0,0])

pur_sp = np.array([[30]] * n) #Pursuer Speed
eva_sp = np.array([[25]] * m) #Evader Speed

asgn = assign.assignment(pur_pos,ev_pos,tar/get,pur_sp,eva_sp) #Assigning the pursuers
asgn.check_win() #Initiating the game
