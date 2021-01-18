#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import JointReques
from std_srvs.srv import Empty

cart_position = 0.0 # m
cart_velocity = 0.0 # rad/s
pole_position = 0.0 # m
pole_velocity = 0.0 # rad/s

def odm_callback(msg):
    global cart_position, cart_velocity
    cart_position = float(msg.pose.pose.position.x)
    cart_velocity = float(msg.twist.twist.linear.x)

def js_callback(msg):
    global pole_position, pole_velocity
    pole_position = msg.position[2]
    pole_velocity = msg.velocity[2]

def init_sim():
    vel = Twist()
    vel.linear.x = 0.0
    pub.publish(vel)
    reset_world

max_episodes = 100
max_steps = 200
Ts = 0.01
rate = rospy.Rate(1.0/Ts)

rospy.init_node('cartpole_controller')
pub = rospy.Publisher('/cartpole/diff_drive_controller/cmd_vel', Twist, queue_size=1)
reset_world = rospy.ServiceProxy('/gazebo/reset_world', Empty)

init_sim()
for episode in range(1, max_episodes+1):
    init_sim()
    print("episode ", episode)
    for istep in range(1, max_steps+1):
        print(istep, "step")
        rate.sleep()

rospy.on_shutdown()
