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
Methodology 

 

Problem Formulation 

We consider a Pursuit – Evasion (PE) game involving n pursuers and m evaders. The primary objective of each evader is to reach a stationary target, assumed without loss of generality to be the origin, while each pursuer’s objective is to prevent the evader from doing so.  

A given evader is denoted by Ei , i ∈ M = (1, 2,…,m) and a given pursuer is denoted by Pj ,                   j ∈ N = (1, 2,...,n).  All players are assumed to be holonomic and interact in 2-dimensional Euclidean space.  

 

The position vectors of evader Ei and a pursuer Pj can be defined as 

$xEi   = (xE, yE) ∈ R2, and xPj = (xp , yp) ∈ R2   for i ∈ M and j ∈ N$

The control inputs for each team are defined by: 

uEi = (uxi, uyi) and vEi = (vxi, vyi) for i ∈ M and j ∈ N. 

The joint control for all evaders and pursuers is denoted by  

Evader - u: = (uE1,...,uEm) 

Pursuer - v: = (vP1,...,vPn) 

We assume that players Ei and Pj move with constant speeds Ui > 0 and Vj > 0 respectively for         i ∈ M and j ∈ N. The speed ratio αij between evader Ei and a pursuer Pj can be defined as 
αij= UiVj
α
ij
=
 
U
i
V
j
 
  which can take any real positive value for all i ∈ M and j ∈ N. 

 

The players have simple motion dynamics given by: 

Text Box 2, TextboxẋEi (t) = uxi (t), ẏEi (t) = uyi (t)  

ẋPj (t) = vxj (t), ẏPj (t) = vyj (t) 

with initial positions xEi (0) = (xEi0 , y Ei0) and xPj (0) = (xPj0 , yPj0) for i ∈ M and j ∈ N. The global initial state is represented as:  x0 = R2(m+n) 
