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

## Sample Outputs

https://github.com/user-attachments/assets/5009c73b-df22-4e88-8857-4c2a0074308e

https://github.com/user-attachments/assets/52e9bb2e-1f2f-45bf-a9dc-383e514ffb93


