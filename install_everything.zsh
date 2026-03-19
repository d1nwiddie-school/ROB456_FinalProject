#!/bin/zsh
# --- ROB456 FINAL PROJECT MASTER INSTALLER V3 ---

echo "🚀 Starting Full System Provisioning..."

# 1. LOCALES & REPO SETUP
sudo apt update && sudo apt install locales curl gnupg2 lsb-release -y
sudo locale-gen en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. ROS 2 KILTED REPO SETUP
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update

# 3. SYSTEM LIBRARIES (PDF Page 1 & 2)
sudo apt install ros-dev-tools ros-kilted-desktop -y
sudo apt install libfltk1.3-dev libjpeg-dev libltdl-dev pkg-config libpng-dev libglu1-mesa-dev -y

# 4. REQUIRED MESSAGE PACKAGES
sudo apt install ros-kilted-marker-msgs ros-kilted-ackermann-msgs ros-kilted-rmw-zenoh-cpp -y

# 5. WAKE UP GLOBAL ROS (CRITICAL FIX)
# This allows colcon to find ament_cmake for your lab packages
source /opt/ros/kilted/setup.zsh

# 6. THE PYTHON EXECUTABLE FIX (PDF Page 1, Note 29-31)
echo "🛠️ Applying Python3_EXECUTABLE fix to Stage and stage_ros2..."
sed -i '2a set(Python3_EXECUTABLE "/usr/bin/python3")' /workspaces/ROB456_FinalProject/src/Stage/CMakeLists.txt
sed -i '2a set(Python3_EXECUTABLE "/usr/bin/python3")' /workspaces/ROB456_FinalProject/src/stage_ros2/CMakeLists.txt

# 7. ROSDEP & LINKER REFRESH
sudo rosdep init || true
rosdep update
sudo ldconfig

# 8. THE SEQUENTIAL SOURCE BUILD (PDF Page 1, Step 21-25)
cd /workspaces/ROB456_FinalProject
rm -rf build install log

echo "🏗️ Building Stage Core..."
colcon build --packages-select Stage --symlink-install

# SOURCE THE NEW STAGE ENGINE SO THE WRAPPER CAN FIND IT
source install/setup.zsh

echo "🏗️ Building everything else (stage_ros2, labs, nav_targets)..."
colcon build --symlink-install

# 9. PERMANENT ENVIRONMENT SETTINGS
echo "source /opt/ros/kilted/setup.zsh" >> ~/.zshrc
echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" >> ~/.zshrc
echo "export DISPLAY=:1" >> ~/.zshrc
echo "source /workspaces/ROB456_FinalProject/install/setup.zsh" >> ~/.zshrc

echo "------------------------------------------------"
echo "✅ SUCCESS: Everything is built and synced."
