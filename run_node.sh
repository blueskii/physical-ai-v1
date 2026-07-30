#!/bin/bash

# 개별 노드 실행을 위해 서비스 중지
# sudo systemctl stop robot.service

# ROS2 환경 설정
source install/setup.bash

# 개별 노드 실행
ros2 run robot $1

# 노드 종료 후 서비스 재시작
# sudo systemctl start robot.service
