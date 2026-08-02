####################################################
# 텍스트와 이미지를 동시에 전달하는 커스텀 메시지 정의
####################################################

# string 타입 필드 선언
string text

# sensor_msgs/Image 타입 필드 선언
# - sensor_msgs/Image: ROS 2 IDL(Interface Definition Language)의 이미지 타입 표기법
# - 매핑되는 실제 타입: sensor_msgs/msg/Image
sensor_msgs/Image image
