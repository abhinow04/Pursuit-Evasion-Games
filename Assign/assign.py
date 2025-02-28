import numpy as np
from scipy.optimize import minimize,linprog
import pandas as pd
from evader import evader
from pursuer import pursuer
class assignment:
    def __init__(self,pursuer_position,evader_position,target_position,speed,pur_sp,eva_sp):

        self.pur_pos = np.array(pursuer_position) #2D positions - nx2
        self.eva_pos = np.array(evader_position) #2D positions - mx2
        self.n = len(self.pur_pos) #Number of pursuers
        self.m = len(self.eva_pos) #Number of evader
        self.pur_sp = pur_sp
        self.eva_sp = eva_sp
        self.mpn = self.m + self.n # m+n
        self.mn = self.m * self.n # m * n
        self.cost = np.zeros([self.mn,self.mpn])
        self.target = target_position #Target Position
        self.val = np.zeros([self.n,self.m]) #Value matrix
        self.B = np.zeros([self.m,self.n]) #Barrier matrix
        self.alpha = self.eva_sp/self.pur_sp #Speed ratio = evader/pursuer
        self.pursuers = [None] * self.n
        self.evaders = [None] * self.m
        print("test")

        for i in range(self.n):
            self.pursuers[i] = pursuer(self.pur_pos[i,:].T,self.pur_sp[i],i)

        for j in range(self.m):
            self.evaders[j] = evader(self.eva_pos[j,:].T,self.eva_sp[j],j)
        
        
    def barrier_region(self):
        nes = np.linalg.norm(self.eva_pos*self.eva_pos,2,1)
        nps = np.linalg.norm(self.pur_pos*self.pur_pos,2,1)
        self.B = nes - nps.T * self.alpha**2
        print("Barrier region\n",self.B)

    def val_mat(self):
        nps = np.sum(self.pur_pos**2, axis=1)
        nes = np.sum(self.eva_pos**2, axis=1)
        alphasq = self.alpha**2
        alpha_factor = self.alpha / (1 - alphasq)

        psh = np.shape(self.pur_pos)
        esh = np.shape(self.eva_pos)
        ash = np.shape(alphasq)

        
        dist1 = np.sqrt(np.sum((np.reshape(self.pur_pos,[psh[0],1,psh[1]]) - np.reshape(self.eva_pos,[1,esh[0],esh[1]]))**2, axis=2))


        v1 = 0.5 * (nes.T - nps / dist1)

        difference = np.reshape(self.eva_pos,[esh[0],1,esh[1]]) - np.reshape(self.pur_pos,[1,esh[0],esh[1]])
        dist2 = np.sqrt(np.sum(difference**2, axis=2))

        alphasq = self.alpha**2
        alpha_factor = self.alpha / (1 - alphasq)

        first_term = np.sqrt(np.sum((np.reshape(self.eva_pos,[esh[0], 1, esh[1]]) - np.reshape(alphasq,[1, ash[0], ash[1]]) * np.reshape(self.pur_pos,[1, psh[0], psh[1]]))**2))
        second_term = alpha_factor * dist2



        v2 = first_term - second_term
        v3 = -np.sqrt(nps.T)+np.sqrt(nes)/self.alpha

        idx1 = (self.B>=0)*(self.alpha==1)
        idx2 = (self.B>=0)*(self.alpha<1)
        idx3 = (self.B<0)*(self.alpha<=1)

        self.val = idx1*v1 + idx2*v2 + idx3*v3

        idx = (self.B>=0) * (self.alpha<=1)
        self.a = idx * self.val
        L = []
        for i in range(np.shape(self.a)[0]):
            L.append(max(self.a[i]))
        L = np.sum(L)

        for i in range(np.shape(self.a)[0]):
            for j in range(np.shape(self.a)[1]):
                if self.a[i][j] == 0:
                    self.a[i][j] = -L-1

        self.a = self.a
        self.linporgram()


    

    def linporgram(self):
        f = self.a.T
        f = np.reshape(f, (np.shape(f)[0] + np.shape(f)[1]))
        print(f)
        b = np.ones([self.mpn, 1])
        A = np.zeros([self.mpn, self.mn])
    
        row_indices = np.arange(self.n, self.n + self.m)
        col_start_indices = (row_indices - self.n) * self.n
        col_indices = np.arange(self.n) + col_start_indices[:, np.newaxis]

        A[row_indices[:, np.newaxis], col_indices] = 1
        A[:self.n, :] = np.tile(np.eye(self.n), (1, self.m))


        bounds = [(0, None) for _ in range(self.mn)]

        if self.n >= self.m:
            x = linprog(-f, A_ub=A[0:self.n, :], b_ub=b[0:self.n],A_eq=A[self.n:self.mpn, :], b_eq=b[self.n:self.mpn], bounds=bounds)
        else:
            x = linprog(-f, A_ub=A[self.n:self.mpn, :], b_ub=b[self.n:self.mpn], A_eq=A[0:self.n, :], b_eq=b[0:self.n], bounds=bounds)

        self.x = np.reshape(x.x, [self.n, self.m]).T

        for i in range(self.m):
            assigned_pursuers = np.where(self.x[i, :] == 1)[0]
            if assigned_pursuers.size > 0:
                self.evaders[i].pursuer = assigned_pursuers.tolist()

        for j in range(self.n):
            assigned_evaders = np.where(self.x[:, j] == 1)[0]
            if assigned_evaders.size > 0:
                self.pursuers[j].evader = assigned_evaders.tolist()
                self.pursuers[j].status = -1



    def check_win(self):
        self.barrier_region()
        self.val_mat()
        self.linporgram()

        [row,columns] = np.where(self.x == 1)
        
        for i in range(len(row)):
            self.evaders[row[i]].pursuer = columns[i]
            
        for j in range(len(columns)):            
            self.pursuers(columns[j]).evader = row[j]

        check = self.a * self.x

        if min(check[:])<0:
            self.win = 1
        else:
            self.win = 0

        mask = (self.alpha>1) * self.x
        if mask.any():
            self.check_cond = 1

        else:
            self.check_cond = 0
        print(self.win)
    def updateStatus(self):
        for i in range(self.m):
            j = self.evader(i).pursuer
            if (np.linalg.norm(self.pursuer[j].position - self.evaders[i].position) < self.tolerance & np.linalg.norm(self.evaders[i].position) > self.tolerance):
                self.evaders[i].status = 1
                self.pursuer[j] = 1
            elif np.linalg.norm(self.evaders[i].position) < self.tolerance:
                self.evaders[i].status = -1

    def termination_status(self):
        if not self.win:
            return all(evader.status == 1 for evader in self.evaders)
        else:
            winning_evaders = np.where(np.sum(self.a * self.x, axis=1) <= 0)[0]
            if not any(-self.evaders[i].status for i in winning_evaders):
                return False
            else:
                return all(self.evaders[i].status == -1 for i in winning_evaders)

    def step(self):
        self.update_status()
        done = self.termination_status()
        
        for i in [index for index, evader in enumerate(self.evaders) if evader.status == 0]:
            j = np.where(self.x[i, :] == 1)[0]
            if j.size > 0:
                self.evaders[i].update_pos(self.evaders[i].position + self.timestep *
                                           self.evaders[i].return_velocity(self.pursuers[j[0]], self.B[i, j[0]], self.tolerance))
        
        for j in [index for index, pursuer in enumerate(self.pursuers) if pursuer.status == -1]:
            i = np.where(self.x[:, j] == 1)[0]
            if i.size > 0:
                self.pursuers[j].update_pos(self.pursuers[j].position + self.timestep *
                                            self.pursuers[j].return_velocity(self.evaders[i[0]], self.B[i[0], j], self.tolerance))

        return done

    def plot_current_positions(self):
        plt.figure()
        plt.scatter(0, 0, color='g', s=100, label='Origin')
        
        for evader in self.evaders:
            plt.scatter(evader.position[0], evader.position[1], color='b', s=100, label='Evader')
        
        for pursuer in self.pursuers:
            plt.scatter(pursuer.position[0], pursuer.position[1], color='r', s=100, label='Pursuer')
        
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def plot_trajectories(self):
        self.check_win()
        self.plot_current_positions()
        done = False
        t = 1
        time_chunk = 1000
        pursuer_traj = np.zeros((2, time_chunk, self.n))
        evader_traj = np.zeros((2, time_chunk, self.m))
        
        while not done:
            pursuer_traj[:, t, :] = np.array([[p.position[0], p.position[1]] for p in self.pursuers]).T
            evader_traj[:, t, :] = np.array([[e.position[0], e.position[1]] for e in self.evaders]).T
            
            if t % 10 == 0:
                plt.pause(0.01)
                plt.clf()
                for j in range(self.n):
                    plt.plot(pursuer_traj[0, :t, j], pursuer_traj[1, :t, j], 'r')
                for i in range(self.m):
                    plt.plot(evader_traj[0, :t, i], evader_traj[1, :t, i], 'b')
                self.plot_current_positions()
            
            done = self.step()
            t += 1
            
            if t > time_chunk:
                pursuer_traj = np.concatenate((pursuer_traj, np.zeros((2, time_chunk, self.n))), axis=1)
                evader_traj = np.concatenate((evader_traj, np.zeros((2, time_chunk, self.m))), axis=1)
        plt.show()



##        c = self.val
##        a = self.cost
##        b = np.ones([1,self.mpn])
##        min_cost = np.linprog(c, A_ub = a , b_ub = b)
