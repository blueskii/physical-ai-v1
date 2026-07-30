#!/bin/bash

# 개별 노드 실행을 위해 서비스 중지
# sudo systemctl stop robot.service

# ROS2 환경 설정
source install/setup.bash

# 로컬 통신만 사용 (DDS discovery 지연 방지 — ROS2 Jazzy 호환)
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST

# 개별 노드 실행
ros2 run robot $1

# 노드 종료 후 서비스 재시작 (Ctrl+C 등으로 종료되어도 실행됨)
# sudo systemctl start robot.service
