import math
import numpy as np
import matplotlib.pyplot as plt

class OmniRobot:
    def __init__(self, pos,ori):
        self.wheel_radius = 2.5/100
        self.robot_radius = 15/100 
        self.position = pos
        self.orientation = ori 
        self.max_yaw_velocity = 1 
        self.max_wheel_speed = 15  
        self.pat = []
        
    def move_to_target(self, velocity, max_speed=1.0, dt=0.1):
        print(np.linalg.norm(velocity))
        if np.linalg.norm(velocity) > 0:
            desired_velocity = np.array([velocity[0], velocity[1], 0])  # Convert to [vx, vy, 0]
            
            wheel_velocities_percent = self.inverse_kinematics(desired_velocity)
            print(wheel_velocities_percent)
            return wheel_velocities_percent
        else:
            return [0, 0, 0]

    def inverse_kinematics(self, velocity):
        velocity = np.array([velocity[0], velocity[1], 0])
        R = self.robot_radius

        jacobian = (1/self.wheel_radius) * np.array([
        [-math.sin(self.orientation), math.cos(self.orientation), R],
        [-math.sin(self.orientation+2*math.pi/3), math.cos(self.orientation+2*math.pi/3), R],
        [-math.sin(self.orientation-2*math.pi/3), -math.cos(self.orientation-2*math.pi/3), R]
        ])
        wheel_velocities = np.dot(jacobian, velocity)
        print(wheel_velocities)
        print("hi")
        wheel_velocities_percent = (wheel_velocities / self.max_wheel_speed) * 100
        if max(abs(wheel_velocities_percent)) > 100:
            wheel_velocities_percent /= (max(abs(wheel_velocities_percent))/30)//1
            
        return wheel_velocities_percent
    
    def update_state(self, wheel_velocities_percent, dt):
        wheel_velocities = (wheel_velocities_percent / 10) * self.max_wheel_speed
        self.orientation = self.orientation
        return wheel_velocities
    
    def forward_kinematics(self, wheel_velocities):
        w1, w2, w3 = wheel_velocities
        vx = self.wheel_radius * (-0.5 * w1 - 0.5 * w2 + w3)
        vy = self.wheel_radius * (-0.866 * w1 + 0.866 * w2)
        return np.array([vx, vy])
    
    def global_to_local(self, global_vector):
        rotation_matrix = np.array([
            [math.cos(self.orientation), math.sin(self.orientation)],
            [-math.sin(self.orientation), math.cos(self.orientation)]
        ])
        return rotation_matrix.dot(global_vector)
    
    def local_to_global(self, local_vector):
        rotation_matrix = np.array([
            [math.cos(self.orientation), -math.sin(self.orientation)],
            [math.sin(self.orientation), math.cos(self.orientation)]
        ])
        return rotation_matrix.dot(local_vector)

    def plott(self):
        print("\n",np.reshape(self.pat,[np.shape(self.pat)[0],2]))
        plt.plot(self.pat)
        plt.show()
