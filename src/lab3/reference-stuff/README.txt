In here I'm going to put a bunch of useful stuff, like how ros2 formats TwistStamped messages, or how the /map occupancy grid is displayed in text form. I'll have pictures of demo .PGMs as well in here to test on, all that good stuff.

BASIC INFO: with ros2 running lab3 via lab3.launch.py, you can view all topics with
$ ros2 topic list
... the unmodified version of our code will then list:
/base_scan
/clicked_point
/clock
/cmd_vel
/current_target
/current_target_array
/goal_points
/goal_pose
/initialpose
/map
/map_metadata
/map_updates
/odom
/parameter_events
/path_points
/pose
/reachable_points
/rosout
/slam_toolbox/feedback
/slam_toolbox/graph_visualization
/slam_toolbox/scan_visualization
/slam_toolbox/transition_event
/slam_toolbox/update
/tf
/tf_static

INFO INFO:
to get more info on top of your info, run:
$ ros2 topic info <name of topic, inclulding the "/">.


