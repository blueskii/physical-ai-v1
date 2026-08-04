#!/bin/bash

# ROS2 환경 설정
source install/setup.bash

# 실행 매개값이 없으면 launch 파일 실행, 
# 있으면 ros2 run 명령으로 개별 노드 실행
if [[ -z "$1" ]]; then
    ros2 launch robot robot.launch.py
else
    ros2 run robot $1
fi
