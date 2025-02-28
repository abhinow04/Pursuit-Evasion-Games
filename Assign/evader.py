import numpy as np

class evader:

    def __init__(self,initPos,speed,index):
        self.index = index
        self.position = initPos
        self.speed = speed
        self.status = 0
        self.pursuer = 0

    def updatePos(self,position):
        sz_input = np.shape(position)
        sz_output = np.shape(self.position)

        if (sz_input != sz_output):
            if sz_input == np.fliplr(sz_ouput):
                self.position = position.T

            else:
                print("Wrong position dimensions. ")
               

        else:
            self.position = position


    def return_velocity(self,pursuer,B,tolerance):
        alpha = self.speed/pursuer.speed
        xp = pursuer.position
        xe = self.position
        xc = (xe - alpha**2 * xp)/(1 - alpha**2)
        Rc = np.linalg.norm(xc)
        rc = (alpha/(1-alpha**2))*np.linalg.norm(xp-xe)

        if B>=0:
            if abs(np.linalg.norm(self.position - pursuer.position))>tolerance:
                gradV = (1/(1-alpha**2))*(xc/Rc - (alpha**2/(1-alpha**2))*((xe-xp)/rc))

                rhoe = np.linalg.norm(gradV)
                velocity = (-self.speed/rhoe)*gradV

            else:
                velocity = np.zeros(2,1)

        elif (B<0):
            if abs(np.linalg.norm(xe))>1e-3:
                gradV = (1/alpha)*(xe/np.linalg.norm(xe))
                rhoe = np.linalg.norm(gradV)
                velocity = (-self.speed/rhoe)*gradV
            else:
                velocity = np.zeros(2,1)

        return velocity
