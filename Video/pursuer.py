import numpy as np

class pursuer:
    def __init__(self,initPos,speed,index):
        self.index = index
        self.position = initPos
        self.speed = speed
        self.status = 0
        self.self = 0

    def updatePos(self,position):
        print(position)
        position = np.array(position).flatten()[:2]
        
        try:
            sz_input = np.shape(position[self.index])
        except:
            sz_input = np.shape(position[0][self.index])
        sz_output = np.shape(self.position)
        
        if (sz_input != sz_output):
            self.position = position.T

        else:
            self.position = position

    def return_velocity(self, evader, B, tolerance):
        alpha = evader.speed / self.speed
        xe = np.array(evader.position).flatten()
        xp = np.array(self.position).flatten()

        xc = (xe - alpha**2 * xp) / (1 - alpha**2)  # Compute intercept point
        Rc = np.linalg.norm(xc)
        
        print(f"Pursuer {self.index} intercept point: {xc}")

        rc = (alpha / (1 - alpha**2)) * np.linalg.norm(xp - xe)
        if B >= 0:
            if np.linalg.norm(xe - xp) > tolerance:
                gradV = (alpha**2 / (1 - alpha**2)) * (-xc / Rc + (1 / (1 - alpha**2)) * ((xe - xp) / rc))
                velocity = (self.speed / np.linalg.norm(gradV)) * gradV
            else:
                velocity = np.zeros((2,))
        else:
            gradV = xp / np.linalg.norm(xp)
            velocity = (-self.speed / np.linalg.norm(gradV)) * gradV

        return velocity

