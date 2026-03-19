# :NOTE !!!! Not relevant to lab3 core function !!!!
# let's write a translation layer manually!!
# this is something I added for debugging so we could write to /cmd_vel while dealing
# ... with the pickiness of stage/stamped twists.

# twistToStamped: takes twist on /cmd_vel_raw --> echoes to /cmd_vel as twistStamped.
# by Michael Dinwiddie

# standard ROS2 imports below:
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
import std_msgs.msg

# now build the relay object class (remember: class==blueprint!)
class StampedRelay(Node): # this means inherit from Node
    def __init__(self):
        super().__init__('stamped_relay') # python idiom, but this should be the node name that shows up now
        
        # now, listen for the unstamped twist:
        self.sub = self.create_subscription(Twist, '/cmd_vel_raw', self.callback, 10) # this callback is what we'll reference to handle it in a sec, right? 10 max queue size 
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10) # no callback... hmm
        
    # define the callback function
    def callback(self, msg): # main function that runs
        # self.get_logger().info(f"IN:  Lin.x={msg.linear.x:.2f}, Ang.z={msg.angular.z:.2f}")
        out_msg = TwistStamped() # what does this do on its own like this?
        # I think this instantiates a TwistStamped object. Below we will define its std variables.
        out_msg.header.stamp = self.get_clock().now().to_msg()
        out_msg.header.frame_id = 'base_link'
        out_msg.twist = msg # what about this one?
        # --> pretty sure this is just encoding the actual twist from /cmd_vel_raw
        self.pub.publish(out_msg)
        timestamp = out_msg.header.stamp.sec
        # self.get_logger().info(f"OUT: Published Stamped Twist at {timestamp}s")
    
# below is some boilerplate stuff:
def main(args=None):
    rclpy.init(args=args)
    node=StampedRelay() # instantiate
    rclpy.spin(node) # this means "don't end the program when this runs ONCE! Stay here and 'spin the wheels' until a callback is triggered again'."
    node.destroy_node() # ??
    rclpy.shutdown()
    
if __name__=='__main__': # entry point stuff: if I run this file directly (python3 run twistToStamped.py), run the main function
    main() # ??
