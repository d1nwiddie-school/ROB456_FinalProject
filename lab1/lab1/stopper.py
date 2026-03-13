#!/usr/bin/env python3

# Bill Smart, smartw@oregonstate.edu
#
# stopper.py
# ASSIGNMENT: Slow the robot to a stop as it approaches a target


# Every Python node in ROS2 should include these lines.  rclpy is the basic Python
# ROS2 stuff, and Node is the class we're going to use to set up the node.
import rclpy
from rclpy.node import Node


# We're going to do some math
import numpy as np

# Header for the twist message
from std_msgs.msg import Header

# Velocity commands are given with Twist messages, from geometry_msgs
from geometry_msgs.msg import TwistStamped

# Laser scans are given with the LaserScan message, from sensor_msgs
from sensor_msgs.msg import LaserScan


class MyStopper(Node):
	def __init__(self):
		# Initialize the parent class, giving it a name.  The idiom is to use the
		# super() class.
		super().__init__('my_stopper')

		# Set up a publisher.  The default topic for Twist messages is cmd_vel.
		self.pub = self.create_publisher(TwistStamped, 'cmd_vel', 10)

		# Set up a subscriber.  The default topic for LaserScan messages is base_scan.
		self.sub = self.create_subscription(LaserScan, 'base_scan', self.callback, 10)

		# GUIDE: Any variables that you want to add can go here
		self.is_stopped = False

	def callback(self, scan):
		# Every time we get a laser scan, calculate the shortest scan distance in front
		# of the robot, and set the speed accordingly.  We assume that the robot is 38cm
		# wide.  This means that y-values with absolute values greater than 19cm are not
		# in front of the robot.  It also assumes that the LiDAR is at the front of the
		# robot (which it actually isn't) and that it's centered and pointing forwards.
		# We can work around these assumptions, but it's cleaner if we don't

		# Pulling out some useful values from scan
		#   Start and top angles of the scan. 0 degrees is in front of the robot
		# Also given: Total number of scans in that range
		angle_min = scan.angle_min
		angle_max = scan.angle_max
		num_readings = len(scan.ranges)

		# GUIDE
		# Use angle min, max, and number of readings to calculate the theta value for each scan
		# This should be a numpy array of length num_readings, that starts at angle_min and ends at angle_max
  		# YOUR CODE HERE
		# 0: we can run:
		# ros2 topic echo /base_scan
		# ... to see what the data looks like. Sample kept below:
		# header:
		# stamp:
		# 	sec: 65
		# 	nanosec: 800000000
		# frame_id: laser
		# angle_min: -1.5707963705062866
		# angle_max: 1.5707963705062866
		# angle_increment: 0.017550796270370483
		# time_increment: 0.0
		# scan_time: 0.0
		# range_min: 0.0
		# range_max: 8.0
		# ranges:
		# - 2.1600000858306885
		# - 2.160332679748535
		# - 2.1613314151763916
		# - 2.1629974842071533
		# - 2.1653337478637695
		# - 2.1683435440063477
		# - 2.172031879425049
		# - 2.1764042377471924
		# - 2.1814675331115723
		# - 2.187229633331299

		# GUIDE: Determine what the closest obstacle/reading is for scans in front of the robot
		#  Step 1: Determine which of the range readings correspond to being "in front of" the robot (see comment at top)
		#    Remember that robot scans are in the robot's coordinate system - theta = 0 means straight ahead
		theta = np.linspace(angle_min, angle_max, num_readings)
		# Filter to only include scans that are in front of the robot (i.e., within 180 degrees of the robot's forward direction)
		
		# she literally said DON'T hardcode the angle
		# life is hard when you're stupid
		bot_width = 0.38
		angle_in_front = np.arcsin(bot_width/2) # == 0.191162 rads
		
		front_indices = np.where(np.abs(theta) < angle_in_front )  # = max angle for 1m hypoteneuse at 0.19m radius (half the robot width)

		front_ranges = np.array(scan.ranges)[front_indices] 
		
		#  Step 2: Get the minimum distance to the closest object (use only scans "in front of" the robot)
		shortest = np.min(front_ranges)
		#  Step 3: Use the closest distance from above to decide when to stop
		if shortest < 1.0:
			is_stopped = True

		else:
			is_stopped = False
		
		#  Step 4: Scale how fast you move by the distance to the closet object (tanh is handy here...)
		speed = 0.2 * np.tanh(shortest-1) # upper bound of 0.2, goes down as approaches wall

		#  Step 5: Make sure to actually stop if close to 1 m
		if shortest < 1.0:
			speed = 0.0
		
		# Suggestion: Do this with a for loop before being fancy with numpy (which is substantially faster)
		# uh oh
		# DO NOT hard-wire in the number of readings, or the min/max angle. You CAN hardwire in the size of the robot

		# Create a twist and fill in all the fields (you will only set t.linear.x).
		t = TwistStamped()
		t.header = Header()
		t.header.frame_id = 'base_link'  # Transform is in the robot's coordinate frame
		t.header.stamp = self.get_clock().now().to_msg()  # What time are we sending this?
		t.twist.linear.x = 0.0 if self.is_stopped else speed
		t.twist.linear.y = 0.0
		t.twist.linear.z = 0.0
		t.twist.angular.x = 0.0
		t.twist.angular.y = 0.0
		t.twist.angular.z = 0.0

		shortest = 0
		max_speed = 0.2
  

		# Send the command to the robot.
		self.pub.publish(t)

		# Print out a log message to the INFO channel to let us know it's working.
		self.get_logger().info(f'Shortest {shortest}, speed {t.twist.linear.x}')



# The idiom in ROS2 is to use a function to do all of the setup and work.  This
# function is referenced in the setup.py file as the entry point of the node when
# we're running the node with ros2 run.  The function should have one argument, for
# passing command line arguments, and it should default to None.
def main(args=None):
	# Initialize rclpy.  We should do this every time.
	rclpy.init(args=args)

	# Make a node class.  The idiom in ROS2 is to encapsulte everything in a class
	# that derives from Node.
	stopper = MyStopper()

	# The spin() call gives control over to ROS2, and it now takes a Node-derived
	# class as a parameter.
	rclpy.spin(stopper)

	# Make sure we shutdown everything cleanly.  This should happen, even if we don't
	# include this line, but you should do it anyway.
	rclpy.shutdown()
	

# If we run the node as a script, then we're going to start here.
if __name__ == '__main__':
	# The idiom in ROS2 is to set up a main() function and to call it from the entry
	# point of the script.
	main()