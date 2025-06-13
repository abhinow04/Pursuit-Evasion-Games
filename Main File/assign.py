import numpy as np
from scipy.optimize import minimize,linprog
import pandas as pd
from evader import evader
from pursuer import pursuer
import matplotlib.pyplot as plt
import gogoal
from ev3_send_val import *
import initialise_game
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
        self.tolerance = 5
        self.timestep = 0.1
        self.target = target_position #Target Position
        self.val = np.zeros([self.n,self.m]) #Value matrix
        self.B = np.zeros([self.m,self.n]) #Barrier matrix
        self.assigned = None
        self.alpha = self.eva_sp/self.pur_sp #Speed ratio = evader/pursuer
        self.pursuers = [None] * self.n #Empty initialisation of n pursuers
        self.evaders = [None] * self.m #Empty initialisation of m evaders


        
        #Initialising the pursuers class variables with the values
        for i in range(self.n):
            self.pursuers[i] = pursuer(self.pur_pos[i,:].T,self.pur_sp[i],i)

        for j in range(self.m):
            self.evaders[j] = evader(self.eva_pos[j,:].T,self.eva_sp[j],j)
    #Defining the barrier region
    def barrier_region(self):
        nes = np.linalg.norm(self.eva_pos*self.eva_pos,2,1)
        nps = np.linalg.norm(self.pur_pos*self.pur_pos,2,1)
        self.B = nes - (nps.T * self.alpha**2)

    #Creating the Value matrix
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

        difference = np.reshape(self.eva_pos,[esh[0],1,esh[1]]) - np.reshape(self.pur_pos,[1,psh[0],psh[1]])
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
        print("Value: ",self.a[1])
        self.linporgram()

    def linporgram(self):
        f = self.a.T
##        print(self.a)
        f = np.reshape(f, np.shape(f)[0] * np.shape(f)[1])
        x = f[0]
        y = f[2]
        f = np.array([x,y])
##        print("Value: ",f)
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

        

    def check_win(self):
        self.barrier_region()
        self.val_mat()
        self.linporgram()

        [row, columns] = np.where(self.x == 1)
        
        for i in range(len(row)):
            self.evaders[row[i]].pursuer = columns[i]
            
        for j in range(len(columns)):            
            self.pursuers[columns[j]].evader = row[j]

        check = self.a * self.x
        check_min = min(np.reshape(check, (len(check) * len(check[0]), 1)))

        if check_min[0] < 0:
            self.win = 1
        else:
            self.win = 0

        mask = (self.alpha > 1) * self.x
        if mask.any():
            self.check_cond = 1


        else:
            self.check_cond = 0
            self.plot_contin()
            
            
    def get_pos(self,robot,index):
        pur_pos,ev_pos = initialise_game.get_positions()
        self.pursuer[self.assigned].updateRposition(pur_pos[self.assigned])
        self.evader.updateRposition(ev_pos)
        print("\n\n\n\n\n")
        print(self.pursuer[self.assigned])
        print(pur_pos)
        

    def plot_contin(self):
        done = False
        t = 0
        time_chunk = 1000       
        pursuer_traj = np.zeros((self.n,time_chunk, 2))
        evader_traj = np.zeros((self.m,time_chunk,2))

        while not done:
            pursuer_traj[:, t, :] = np.array([p.position.T for p in self.pursuers])
            evader_traj[:, t, :] = np.array([e.position.T for e in self.evaders])

            plt.clf()


            for j in range(self.n):
                plt.plot(pursuer_traj[j, :t+1, 0], pursuer_traj[j, :t+1, 1], 'r', label="Pursuer" if j == 0 else "")
                plt.scatter(self.pursuers[j].position[0], self.pursuers[j].position[1], color='r', marker='o', s=100)


            for i in range(self.m):
                plt.plot(evader_traj[i, :t+1, 0], evader_traj[i, :t+1, 1], 'b', label="Evader" if i == 0 else "")
                plt.scatter(self.evaders[i].position[0], self.evaders[i].position[1], color='b', marker='x', s=100)


            plt.scatter(0, 0, color='g', s=100, label="Target")


            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.title("Live Pursuer-Evader Trajectory")
            plt.legend()
            plt.grid(True)
    
            plt.pause(0.0000000000000000000000000000000001)
            E_statuses = [e.status for e in self.evaders]
            for i in range(len(E_statuses)):
                if E_statuses[i] == 0:
                    E_statuses[i] = str(i+1)+": Not captured"
                elif E_statuses[i] == 1:
                    E_statuses[i] = str(i+1)+": Captured"
                elif E_statuses[i] == 2:
                    E_statuses[i] = str(i+1)+": Target Breached"
            print("\n\n--- Updating Status ---")

            print(f"Step {t}: \n{E_statuses}")

            all_captured = all(e.status == 1 for e in self.evaders)

            if all_captured:

                print("All evaders captured. Terminating simulation.")
                break              

            done = self.step()
            
            t+=1
                
            if t >= pursuer_traj.shape[1]:  
                pursuer_traj = np.concatenate((pursuer_traj, np.zeros((self.n, time_chunk, 2))), axis=1)
                evader_traj = np.concatenate((evader_traj, np.zeros((self.m, time_chunk, 2))), axis=1)
        plt.show()



    def plot_continR(self):
        done = False
        t = 0
        time_chunk = 1000       
        pursuer_traj = np.zeros((self.n,time_chunk, 2))
        evader_traj = np.zeros((self.m,time_chunk,2))

        while not done:
            pursuer_traj[:, t, :] = np.array([p.rposition.T for p in self.pursuers])
            evader_traj[:, t, :] = np.array([e.rposition.T for e in self.evaders])

            plt.clf()


            for j in range(self.n):
                plt.plot(pursuer_traj[j, :t+1, 0], pursuer_traj[j, :t+1, 1], 'r', label="Pursuer" if j == 0 else "")
                plt.scatter(self.pursuers[j].position[0], self.pursuers[j].position[1], color='r', marker='o', s=100)


            for i in range(self.m):
                plt.plot(evader_traj[i, :t+1, 0], evader_traj[i, :t+1, 1], 'b', label="Evader" if i == 0 else "")
                plt.scatter(self.evaders[i].position[0], self.evaders[i].position[1], color='b', marker='x', s=100)


            plt.scatter(0, 0, color='g', s=100, label="Target")


            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.title("Live Pursuer-Evader Trajectory")
            plt.legend()
            plt.grid(True)
    
            plt.pause(0.0000000000000000000000000000000001)
            E_statuses = [e.status for e in self.evaders]
            for i in range(len(E_statuses)):
                if E_statuses[i] == 0:
                    E_statuses[i] = str(i+1)+": Not captured"
                elif E_statuses[i] == 1:
                    E_statuses[i] = str(i+1)+": Captured"
                elif E_statuses[i] == 2:
                    E_statuses[i] = str(i+1)+": Target Breached"
            print("\n\n--- Updating Status ---")

            print(f"Step {t}: \n{E_statuses}")

            all_captured = all(e.status == 1 for e in self.evaders)

            if all_captured:

                print("All evaders captured. Terminating simulation.")
                break              

            done = self.step()
            
            t+=1
                
            if t >= pursuer_traj.shape[1]:  
                pursuer_traj = np.concatenate((pursuer_traj, np.zeros((self.n, time_chunk, 2))), axis=1)
                evader_traj = np.concatenate((evader_traj, np.zeros((self.m, time_chunk, 2))), axis=1)
        plt.show()



    def updateStatus(self):
        
        for i, evader in enumerate(self.evaders):
            j = evader.pursuer
            if j is not None or isinstance(j, int):

                pursuer = self.pursuers[j]
                distance = np.linalg.norm(pursuer.position - evader.position)
                distance1 = np.linalg.norm(evader.position - self.target)

                if distance < self.tolerance:
                    evader.status = 1
                    pursuer.status = 1

                elif distance1 < self.tolerance:
                    evader.status = 2
                    pursuer.status = 1


    def updateRstatus(self):
        for i,evader in enumerate(self.evaders):
            j = evader.pursuer
            if j is not None or isinstance(j, int):
                pursuer = self.pursuers[j]
                distance = np.linalg.norm(pursuer.rposition - evader.rposition)
                distance1 = np.linalg.norm(evader.rposition - self.target)

                if distance < self.rtolerance:
                    evader.status = 5
                    pursuer.status = 5

                elif distance1 < self.tolerance:
                    evader.status = 4
                    pursuer.status = 5


    def step(self):

        self.updateStatus()
        print("Step: Updating positions")
        if all(e.status == 1 for e in self.evaders):
            print("assigned: ",self.assigned)
            print("All evaders captured. Stopping simulation.")
            return True  

        elif any(e.status == 2 for e in self.evaders):
            print(f"Evader has breached the target point")
            return True

        for i, evader in enumerate(self.evaders):
            if evader.status == 0:
                j = np.where(self.x[i, :] == 1)[0]
                if j.size > 0:
                    eva_retVel = evader.return_velocity(self.pursuers[j[0]], self.B[i, j[0]], self.tolerance)
                    evader.updatePos(evader.position + self.timestep * eva_retVel)

                    
        for j, pursuer in enumerate(self.pursuers):
            if pursuer.status == 0:
                i = np.where(self.x[:, j] == 1)[0]

                if i.size > 0:
                    self.assigned = i[0]
                    pur_retVel = pursuer.return_velocity(self.evaders[i[0]], self.B[i[0], j], self.tolerance)
                    pursuer.updatePos(pursuer.position + self.timestep * pur_retVel)
               
        return False

    def r_step(self):
        self.updateRstatus()
        print("Step: Updating positions")
        if all(e.rstatus == 5 for e in self.evaders):
            print("All evaders captured. Stopping all robots")
            return True

        elif any(e.rstatus == 4 for e in self.evaders):
            print("Evader has breached the targer point. Stopping all robots")
            return True

        for i, evader in enumerate(self.evaders):
            if evader.status == 3:
                j = np.where(self.x[i,:] == 1)[0] 
                if j.size>0:
                    eva_retVel = evader.return_rvelocity(self.pursuers[self.assigned],self.B[i,self.assigned],self.tolerance)
                    
                    self.get_pos()
                    wheele = gogoal.OmniRobot(evader.rposition).move_to_target(eva_retVel)
                    print("Evader wheel velocity: ",wheele)
                    send_vel("evader",wheele)

        
        for j, pursuer in enumerate(self.pursuers):
            if pursuer.status == 3:
                i = np.where(self.x[:, j] == 1)[0]
    
                if i.size > 0:
                    self.assigned = i[0]
                    self.get_pos()                    
                    pur_retVel = pursuer.return_rvelocity(self.evaders[i[0]], self.B[i[0], j], self.tolerance)
                    wheelp = gogoal.OmniRobot(pursuer.rposition).move_to_target(pur_retVel)
                    print("Pursuer wheel velocity: ",wheelp)
                    send_vel("pursuer"+str(j),wheelp)
            elif pursuer.status == 5:
                break
