############################################
# 다양한 타입의 필드를 갖는 커스텀 메시지 타입
# 형식: <type> <field_name>
############################################

# string 타입의 필드 선언
string text

# sensor_msgs/Image 타입의 필드 선언
# - sensor_msgs/Image: ROS 2 IDL(Interface Definition Language)의 이미지 타입 표기법
# - 매핑되는 실제 타입: sensor_msgs/msg/Image
sensor_msgs/Image image
