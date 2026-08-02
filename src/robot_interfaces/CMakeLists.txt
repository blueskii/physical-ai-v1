# CMake 최소 버전 요구 (ROS 2 Jazzy 기준 3.8 이상)
cmake_minimum_required(VERSION 3.8)

# 이 패키지의 이름 선언 (package.xml의 <name>과 반드시 일치해야 함)
# PROJECT_NAME 변수에 패키지 이름이 자동으로 할당됨
project(robot_interfaces)

# ament_cmake: ROS 2 CMake 빌드 시스템 기반 패키지
find_package(ament_cmake REQUIRED)

# rosidl_default_generators: .srv/.msg/.action 파일을 Python/C++ 코드로 변환하는 생성기
find_package(rosidl_default_generators REQUIRED)

# sensor_msgs: TextImage.msg 에서 sensor_msgs/Image 타입을 사용하므로 필요
find_package(sensor_msgs REQUIRED)

# 빌드할 인터페이스 파일 목록 등록
# - 여기에 등록된 .srv 파일이 Python 클래스(robot_interfaces.srv.LedSet 등)로 자동 변환됨
# - 새 인터페이스 추가 시 이 목록에 경로를 추가하면 됨
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TextImage.msg" # 텍스트 + 이미지 복합 메시지
  "srv/LedSet.srv"    # LED 제어 서비스 (state + brightness → success + message)
  "srv/LedGet.srv"    # LED 상태 조회 서비스 (없음 → state + brightness + message)
  DEPENDENCIES sensor_msgs  # TextImage.msg에서 sensor_msgs/Image 참조
)

# 패키지 마무리 선언 (ament 빌드 시스템에 이 패키지를 등록)
ament_package()
