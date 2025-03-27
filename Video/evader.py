import numpy as np

class evader:
    def __init__(self,initPos,speed,index):
        self.index = index
        self.position = initPos
        self.speed = speed
        self.status = 0
        self.pursuer = 0

    def updatePos(self,position):
        
        if (self.status==0):
            position = np.array(position).flatten()[:2]
            sz_input = np.shape(position[self.index])
            sz_output = np.shape(self.position)
            #print("Eva_pos: ",position)
            if (sz_input != sz_output):
                self.position = position.T
                   
            else:
                self.position = position
        else:
            print("Evader has been captured")

    def return_velocity(self, pursuer, B, tolerance):
        alpha = self.speed / pursuer.speed
        xp = pursuer.position
        xe = self.position
        xc = (xe - alpha**2 * xp) / (1 - alpha**2)  # Intercept point calculation
        Rc = np.linalg.norm(xc)

        print(f"Evader {self.index} intercept point: {xc}")

        rc = (alpha / (1 - alpha**2)) * np.linalg.norm(xp - xe)
        if B >= 0:
            if np.linalg.norm(self.position - pursuer.position) > tolerance:
                gradV = (1 / (1 - alpha**2)) * (xc / Rc - (alpha**2 / (1 - alpha**2)) * ((xe - xp) / rc))
                rhoe = np.linalg.norm(gradV)
                velocity = (-self.speed / rhoe) * gradV
            else:
                velocity = np.zeros((1, 2))
        else:
            if np.linalg.norm(xe) > 1e-2:
                gradV = (1 / alpha) * (xe / np.linalg.norm(xe))
                rhoe = np.linalg.norm(gradV)
                velocity = (-self.speed / rhoe) * gradV
            else:
                velocity = np.zeros((1, 2))

        return velocity
