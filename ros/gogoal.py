import math
import numpy as np
import matplotlib.pyplot as plt

class OmniRobot:
    def __init__(self, pos,ori):
        self.wheel_radius = 1
        self.robot_radius = 1
        self.position = pos
        self.orientation = ori # Convert to radians
        self.max_wheel_speed = 15  # Maximum wheel speed in rad/s
        self.pat = []
    def move_to_target(self, target_position, max_speed=1.0, dt=0.1):
        if not np.allclose(self.position, target_position, atol=0.01):

            direction = target_position - self.position
            distance = np.linalg.norm(direction)
          
            velocity = direction / distance * min(max_speed, distance / dt)
          
            local_velocity = self.global_to_local(velocity)
           
            wheel_velocities_percent = self.inverse_kinematics(local_velocity)

            self.update_state(wheel_velocities_percent, dt)
            self.pat.append(self.position)
            print(f"Current position: {self.position}, Target: {target_position}")
            print(f"Wheel velocities (%): {wheel_velocities_percent}")
            return wheel_velocities_percent
        else:
            return [0,0,0]
    
    def inverse_kinematics(self, velocity):
        vx, vy = velocity
        wheel_velocities = np.array([
            -0.5 * vx - 0.866 * vy,
            -0.5 * vx + 0.866 * vy,
            vx
        ]) / self.wheel_radius
        

        wheel_velocities_percent = (wheel_velocities / self.max_wheel_speed) * 100
        
        #wheel_velocities_percent = np.clip(wheel_velocities_percent, -100, 100)
        
        return wheel_velocities_percent
    
    def update_state(self, wheel_velocities_percent, dt):
        # Convert percentage back to rad/s
        wheel_velocities = (wheel_velocities_percent / 100) * self.max_wheel_speed
        local_velocity = self.forward_kinematics(wheel_velocities)
        global_velocity = self.local_to_global(local_velocity)
        self.position += global_velocity * dt
    
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

