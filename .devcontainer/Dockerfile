# virtual environment so EVERYONE is on the same page
# no more cross-device compatibility issues
# Use Ubuntu 24.04 as the base for ROS 2 Kilted
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Set up environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV ROS_DISTRO=kilted
ENV RMW_IMPLEMENTATION=rmw_zenoh_cpp

# 1. Install ROS 2 Kilted and Tooling
RUN apt-get update && apt-get install -q -y \
    curl \
    gnupg2 \
    lsb-release \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 2. Install the Lab 3 Requirements
RUN apt-get update && apt-get install -y \
    ros-kilted-desktop \
    ros-kilted-stage-ros2 \
    ros-kilted-slam-toolbox \
    ros-kilted-nav2-map-server \
    ros-kilted-rmw-zenoh-cpp \
    python3-colcon-common-extensions \
    python3-numpy \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# 3. Source ROS and your workspace automatically for everyone
RUN echo "source /opt/ros/kilted/setup.bash" >> /etc/bash.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" >> /etc/bash.bashrc
