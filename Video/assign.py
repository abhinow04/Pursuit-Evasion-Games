import numpy as np
from scipy.optimize import minimize,linprog
import pandas as pd
from evader import evader
from pursuer import pursuer
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

        self.alpha = self.eva_sp/self.pur_sp #Speed ratio = evader/pursuer
        self.pursuers = [None] * self.n #Empty initialisation of n pursuers
        self.evaders = [None] * self.m #Empty initialisation of m evaders
        self.cap_point = [None]
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
        self.linporgram()

    def linporgram(self):
        f = self.a.T

        f = np.reshape(f, np.shape(f)[0] + np.shape(f)[1])
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


    def plot_contin(self, save_path="pursuit_simulation_4K.mp4"):
        fig, ax = plt.subplots(figsize=(38.4, 21.6), dpi=100)  # 4K Resolution

        ax.set_xlim(-100, 100)  
        ax.set_ylim(-100, 100)

        grid_linewidth = 10  # Uniform grid thickness
        axis_fontsize = 60     # Font size for labels
        marker_size = 3000      # Dot size
        line_width = 16         # Line thickness

        ax.grid(True, linewidth=grid_linewidth)
##        ax.set_title("Pursuit Evasion Games", fontsize=axis_fontsize, fontweight="bold")
        ax.set_xlabel("X axis", fontsize=axis_fontsize)
        ax.set_ylabel("Y axis", fontsize=axis_fontsize)
        ax.tick_params(axis='both', which='major', labelsize=axis_fontsize, width=grid_linewidth)
        ax.set_xticks(np.arange(-100, 120, 20))
        ax.set_yticks(np.arange(-100, 120, 20))

        pursuer_lines = [ax.plot([], [], 'r-', lw=line_width, label="Pursuer" if i == 0 else "")[0] for i in range(self.n)]
        pursuer_dots = [ax.scatter([], [], color='r', marker='o', s=marker_size) for _ in range(self.n)]

        evader_lines = [ax.plot([], [], 'b-', lw=line_width, label="Evader" if i == 0 else "")[0] for i in range(self.m)]
        evader_dots = [ax.scatter([], [], color='b', marker='*', s=marker_size) for _ in range(self.m)]

        target_dot = ax.scatter(0, 0, color='g', s=marker_size, label="Target")

        # Capture points (red stars ⭐)
        capture_points = [ax.scatter([], [], color='red', marker='*', s=marker_size * 1.5) for _ in range(self.m)]

        pursuer_traj = [[] for _ in range(self.n)]
        evader_traj = [[] for _ in range(self.m)]

        def update(frame):
            if self.step():  # Stops the animation if the game ends
                print("🎬 Game Over. Stopping animation.")
                ani.event_source.stop()
                return

            for j, pursuer in enumerate(self.pursuers):
                pursuer_traj[j].append(pursuer.position.copy())
                x_data, y_data = zip(*pursuer_traj[j])
                pursuer_lines[j].set_data(x_data, y_data)
                pursuer_dots[j].set_offsets([pursuer.position[0], pursuer.position[1]])

            for i, evader in enumerate(self.evaders):
                evader_traj[i].append(evader.position.copy())
                x_data, y_data = zip(*evader_traj[i])
                evader_lines[i].set_data(x_data, y_data)
                evader_dots[i].set_offsets([evader.position[0], evader.position[1]])

                # Show capture point if evader is caught
                if evader.status == 1 and hasattr(evader, 'capture_point'):
                    capture_points[i].set_offsets([evader.capture_point[0], evader.capture_point[1]])

            return pursuer_lines + pursuer_dots + evader_lines + evader_dots + capture_points

        ani = animation.FuncAnimation(fig, update, frames=1000, interval=100, blit=False)

        print("🎥 Saving 4K simulation video... This might take a while.")
        
        try:
            ani.save(save_path, writer=animation.FFMpegWriter(fps=10, bitrate=30000))
            print(f"✅ 4K Simulation saved successfully as {save_path}")
        except Exception as e:
            print(f"❌ Error saving video: {e}")

        plt.legend(fontsize=axis_fontsize)
        plt.show()



    def updateStatus(self):
        print("\n--- Updating Status ---")

        for i, evader in enumerate(self.evaders):
            j = evader.pursuer
            if j is not None and isinstance(j, int):  # Ensure valid pursuer index
                pursuer = self.pursuers[j]
                distance = np.linalg.norm(pursuer.position - evader.position)

                if distance < self.tolerance:  # Capture condition
                    evader.status = 1  # Mark evader as captured
                    pursuer.status = 1  # Mark pursuer as successful
                    
                    # Capture point
                    capture_point = evader.position.copy()
                    print(f"⚡ Evader {i} captured at: {capture_point}")

                    # Save the capture point for visualization
                    evader.capture_point = capture_point

    def step(self):
        print("🔄 Step: Updating positions")
        self.updateStatus()  # Updates the status of evaders and pursuers

        # ✅ Stop the game if ALL evaders are captured
        if all(e.status == 1 for e in self.evaders):
            print("✅ All evaders captured. Stopping simulation.")
            return True  

        # ✅ Stop the game if ANY evader reaches the target
        if any(e.status == 2 for e in self.evaders):
            print("🚨 An evader reached the target! Game Over.")
            return True  

        # 🚨 Check if no movement is happening (to prevent infinite loops)
        evaders_still_moving = any(e.status == 0 for e in self.evaders)
        pursuers_still_moving = any(p.status == 0 for p in self.pursuers)

        if not evaders_still_moving and not pursuers_still_moving:
            print("⛔ No movement detected! Stopping simulation to prevent infinite loop.")
            return True

        # Move evaders **only if they are NOT captured**
        for i, evader in enumerate(self.evaders):
            if evader.status == 0:  # Move only if evader is still active
                j = np.where(self.x[i, :] == 1)[0]
                if j.size > 0:
                    velocity = evader.return_velocity(self.pursuers[j[0]], self.B[i, j[0]], self.tolerance)
                    evader.updatePos(evader.position + self.timestep * velocity)

        # Move pursuers **only if they are NOT successful yet**
        for j, pursuer in enumerate(self.pursuers):
            if pursuer.status == 0:  
                i = np.where(self.x[:, j] == 1)[0]
                if i.size > 0:
                    velocity = pursuer.return_velocity(self.evaders[i[0]], self.B[i[0], j], self.tolerance)
                    pursuer.updatePos(pursuer.position + self.timestep * velocity)

        return False  # Continue simulation
