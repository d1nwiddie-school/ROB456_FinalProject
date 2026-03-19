# run this in a NEW terminal window to control the bot with your keyboard
echo "starting with initial ros2 topics:"
ros2 topic list
echo "adding /cmd_vel_raw and starting twistToStamped relay node"

python3 twistToStamped.py &
# store the PID of the background process so we can kill it later
BRIDGE_PID=$!
# IF THIS FAILS: check which python environment python3 defaults to, make sure it's linked to your ros install
# ... since the node depends on rclpy.

echo "success, starting teleop_twist:"
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/cmd_vel_raw


# 4. Run the teleop keyboard in the foreground
# This keeps the terminal active so you can actually type
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# on Ctrl+C, kill the background bridge
echo "shutting down..."
kill $BRIDGE_PID