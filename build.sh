#!/bin/bash

# 서비스 중지
# sudo systemctl stop robot.service

# ROS2 패키지 빌드
source /opt/ros/jazzy/setup.bash
colcon build

# 서비스 재시작
# sudo systemctl restart robot.service
