import numpy as np
import assign
import initialise_game

N = 2
n = 2
m = 1   
v = np.ones(m)
u = np.ones(n)
r = 1

#pur_pos, ev_pos = initialise_game.get_positions()
pur_pos = [[0.35345,0.33438],[0.645634,0.234543]]
ev_pos = [[0.324235,0.342353]]
##print("Pursuer position: ", pur_pos)
##print("Evader position: ", ev_pos)

target = np.array([0, 0])

pur_sp = np.array([[0.03]] * n)
eva_sp = np.array([[0.025]] * m)

asgn = assign.assignment(pur_pos, ev_pos, target, v, pur_sp, eva_sp)
asgn.check_win()
