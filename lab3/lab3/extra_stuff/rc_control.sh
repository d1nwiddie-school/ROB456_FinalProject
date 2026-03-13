# run this in a NEW terminal window to control the bot with your keyboard
echo "starting with initial ros2 topics:"
ros2 topic list
echo "adding /cmd_vel_raw and starting twistToStamped relay node"
python3 twistToStamped.py
# IF THIS FAILS: check which python environment python3 defaults to, make sure it's linked to your ros install
# ... since the node depends on rclpy.
echo "success, starting teleop_twist:"
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/cmd_vel_raw