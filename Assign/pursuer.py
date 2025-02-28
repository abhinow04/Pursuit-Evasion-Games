import numpy as np

class pursuer:
    def __init__(self,initPos,speed,index):
        self.index = index
        self.position = initPos
        self.speed = speed
        self.status = 0
        self.self = 0

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


    def return_velocity(self,evader,B,tolerance):
        alpha = evader.speed/self.speed
        xe = evader.position
        xp = self.position
        xc = (xe - alpha**2 * xp)/(1 - alpha**2)
        Rc = np.linalg.norm(xc)
        rc = (alpha/(1-alpha**2))*np.linalg.norm(xp-xe)

        if B>=0:
            if abs(np.linalg.norm(evader.position - self.position))>tolerance:
                gradV = (alpha**2/(1-alpha**2))*(-xc/Rc+(1/(1-alpha**2))*((xe-xp)/rc))

                rhop = np.linalg.norm(gradV)
                velocity = (self.speed/rhop)*gradV

            else:
                velocity = np.zeros(2,1)

        elif (B<0):
            if abs(np.linalg.norm(xe))>1e-3:
                gradV = xp/np.linalg.norm(xp)
                rhoe = np.linalg.norm(gradV)
                velocity = (-self.speed/rhop)*gradV
            else:
                velocity = np.zeros(2,1)

        return velocity
