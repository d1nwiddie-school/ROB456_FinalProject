# NOTE 1: USE THIS INSIDE THE CODESPACE IF SOMEBODY FUCKS SOMETHING UP
# NOTE 2: PLEASE DON'T FUCK THE CODESPACE UP

#!/zsh
# install_everything.zsh - The "No More snags" Installer

echo "🚀 Starting Full Kaiju Provisioning..."

# 1. FIX LOCALES & REPOS
sudo apt update && sudo apt install locales curl gnupg2 lsb-release -y
sudo locale-gen en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. ROS 2 KILTED KEYS
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update

# 3. INSTALL SYSTEM DEPENDENCIES (FLTK, MESA, MSGS)
sudo apt install ros-dev-tools ros-kilted-desktop -y
sudo apt install libfltk1.3-dev pkg-config libpng-dev libjpeg-dev libglu1-mesa-dev libltdl-dev -y
sudo apt install ros-kilted-marker-msgs ros-kilted-ackermann-msgs ros-kilted-rmw-zenoh-cpp -y

# 4. INITIALIZE ROSDEP
sudo rosdep init || true
rosdep update

# 5. FIX THE ZENOH LINKER ERROR
sudo ldconfig

# 6. CONFIGURE ZSH PERMANENTLY
echo "source /opt/ros/kilted/setup.zsh" >> ~/.zshrc
echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" >> ~/.zshrc
echo "export DISPLAY=:1" >> ~/.zshrc

# 7. THE BIG BUILD
cd /workspaces/ROB456_FinalProject
rm -rf build install log
colcon build --symlink-install
source install/setup.zsh

echo "✅ SETUP COMPLETE. Open Port 6080 in your browser and run your launch file."
