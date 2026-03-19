# NOTE 1: USE THIS INSIDE THE CODESPACE IF SOMEBODY FUCKS SOMETHING UP
# NOTE 2: PLEASE DON'T FUCK THE CODESPACE UP

#!/bin/bash

# --- ROS 2 Kilted Kudu / Kaiju Install Script ---
# Compiled from d1nwiddie's terminal logs - March 2026

echo "Starting ROS 2 Kilted Installation..."

# 1. SET UP LOCALES (Ensuring UTF-8)
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. ADD THE ROS 2 REPOSITORY
# We need the GPG key to verify the packages
sudo apt install curl gnupg2 lsb-release -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add the repository to your sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 3. UPDATE & INSTALL TOOLS
sudo apt update
sudo apt install ros-dev-tools -y

# 4. INSTALL ROS KILTED DESKTOP
# This includes RViz, which we need for the noVNC desktop
sudo apt install ros-kilted-desktop -y

# 5. INSTALL LAB 3 SPECIFIC PACKAGES
# Using the naming fix we identified earlier
sudo apt install ros-kilted-stage-ros ros-kilted-slam-toolbox ros-kilted-nav2-map-server ros-kilted-rmw-zenoh-cpp -y

# 6. ENVIRONMENT SETUP
echo "source /opt/ros/kilted/setup.bash" >> ~/.bashrc
echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" >> ~/.bashrc

echo "------------------------------------------------"
echo "Installation complete! Source your .bashrc or restart your terminal."
echo "Then, run 'ros2' to verify."
