#!/bin/bash

# 서비스 중지
# sudo systemctl stop robot.service

# ROS2 패키지 빌드
colcon build

# 서비스 재시작
# sudo systemctl restart robot.service

# 서비스 로그 실시간 확인
# sudo journalctl -u robot.service -f 
