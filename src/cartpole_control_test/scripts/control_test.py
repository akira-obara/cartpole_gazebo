#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState

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

rospy.init_node('cartpole_controller')
pub = rospy.Publisher('/cartpole/diff_drive_controller/cmd_vel', Twist, queue_size=1)
odm_sub = rospy.Subscriber('/cartpole/diff_drive_controller/odom', Odometry, odm_callback)
js_sub  = rospy.Subscriber('/cartpole/joint_states', JointState, js_callback)

while not rospy.is_shutdown():
    vel = Twist()
    direction = raw_input('w: forward, s: backward, a: left, d: right > ')
    if 'w' in direction:
        vel.linear.x = 0.3
    if 's' in direction:
        vel.linear.x = -0.3
    if 'a' in direction:
        vel.angular.z = 0.3
    if 'd' in direction:
        vel.angular.z = -0.3
    if 'q' in direction:
        break
    print vel
    pub.publish(vel)
    print("cart_position: ", cart_position)
    print("cart_velocity: ", cart_velocity)
    print("pole_position: ", pole_position)
    print("pole_velocity: ", pole_velocity)
