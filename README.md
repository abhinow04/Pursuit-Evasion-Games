# Pursuit - Evasion Games

This repository presents the implementation and experimental validation of a real-time 2-pursuer, 1-evader pursuit-evasion game using holonomic mobile robots constructed from LEGO EV3 kits. The robot configuration enables omnidirectional motion, providing enhanced manoeuvrability in a bounded 2D arena. The motion of all agents is tracked using a high-precision OptiTrack motion capture system. Control decisions are computed in real-time on a central computer using ROS 2 Jazzy, while inter-device communication with the robots is handled via the MQTT protocol to ensure efficient publish-subscribe messaging.

## Problem Overview
Security breaches are becoming a growing concern across multiple sectors, including corporate environments, industrial facilities, and even residential neighbourhoods. Traditional reliance on human security personnel, while valuable, often falls short due to limitations such as restricted working hours, susceptibility to fatigue, delayed response times, and high operational costs. As the demand for more efficient, reliable, and round-the-clock surveillance increases, there is a pressing need to explore automated alternatives.

## Setup
The setup involved fitting the Lego robots with omnidirectional wheels which provided holonomic motion, i.e., allowed the robot to move 360˚ without the need for orientation change. The robot was constructed with 3-wheel design with each wheel mutually placed at 120˚ from each other. The robots were programmed to receive the wheel speed ratios using an Mosquitto net MQTT server over a LAN connection. The robot was driven using a Lego EV3 Large Servo Motor and had the following specifications:
- **Type:** Tacho motor with built-in rotation sensor
- **Rotation sensor resolution:** +/- 1˚
- **Torque:** Up to 40 Ncm
- **Speed (No load):** Up to 160 RPM
- **Operating Voltage:** 6V to 9V

The EV3 brick used as the CPU for the robot was fitted with the following hardware:
- **Processor:** Samsung 64mb RAM processor
- **Clock Speed:** 300 MHz

<img width="253" height="271" alt="Screenshot from 2026-05-29 20-35-17" src="https://github.com/user-attachments/assets/29cc1438-2ad1-4289-a53c-e792d5a4a18c" />

<img width="235" height="271" alt="image" src="https://github.com/user-attachments/assets/131e462a-c5ea-4a50-bbb5-845fecfcb3e3" />

## Cloning
```bash
git clone https://github.com/abhinow04/Pursuit-Evasion-Games.git
```
### Modules
Require python modules include
- Pandas
- Matplotlib
- Numpy
- Rclpy

## Methodology
[Methodology.pdf](https://github.com/user-attachments/files/28409046/Methodology.pdf)

## Results
The simulations were completely performed within the python environment using live animation tool in the Matplotlib library. It was observed that the algorithm can be expanded to any number of pursuers and evaders given that the number of pursuers taken is greater than or equal to the number of evaders (n >= m). The initial positions are randomised using random tool in numpy library in python which leads to the observation that the algorithm works successfully for any given position of the robots and the assignment is precisely done.

<img width="1920" height="1080" alt="Screenshot from 2025-05-06 13-54-44" src="https://github.com/user-attachments/assets/8313e468-922a-4d85-b216-89ea038c32ab" />

Consider the PE game with 2 pursuers and 1 evader. The pursuers are starting at the positions 𝑥𝑝1 = (393.3885 , 298.4631) and 𝑥𝑝2 = (−68.4496 , −206.2937) while the evader is at 𝑥𝑒 = (−62.8854 , 43.3758). The pursuer speeds are set at 30 while the evader speeds are set at 20. It is observed that for this particular arrangement, pursuer 2 has been assigned to chase the evader. The game is a evader winning scenario and it is observed that the optimal path for the pursuer is to move towards the target point (the origin) and at terminal time, the pursuer is at point which is the closest it can be with respect to the origin with respect to its starting position.

<img width="1920" height="1080" alt="Screenshot from 2025-05-06 13-52-57" src="https://github.com/user-attachments/assets/015eea40-216c-4cc6-951e-3662c6affeff" />

Consider the PE game with 2 pursuers and 1 evader. The pursuers are starting at the positions 𝑥𝑝1 = (357.4483 , 179.4571) and 𝑥𝑝2 = (−508.5739 , 370.4696) while the evader is at 𝑥𝑒 = (−223.5273 , 356.2219). The pursuer speeds are set at 30 while the evader speeds are set at 20. It is observed that for this particular arrangement, the value of the game is found to be 173.3219 and pursuer 1 has been assigned to chase the evader. The game is a evader winning scenario and it is observed that the optimal path for the pursuer is to move towards the target point (the origin) and at terminal time, the pursuer is at point which is the closest it can be with respect to the origin with respect to its starting position.

<img width="1920" height="1080" alt="Screenshot from 2025-05-06 13-55-22" src="https://github.com/user-attachments/assets/d95978da-ca87-457b-8bfb-4f9221f6cafe" />

## References
