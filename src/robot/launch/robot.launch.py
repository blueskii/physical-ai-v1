from launch import LaunchDescription      # 실행할 노드 목록을 담는 컨테이너
from launch_ros.actions import Node       # 개별 노드 실행 설정

# ROS 2 시스템이 한번에 실행할 노드들을 LaunchDescription에 포장해서 리턴하는 함수
# - ros2 launch robot robot.launch.py 명령으로 호출
def generate_launch_description():
    return LaunchDescription([
            # 새 노드 추가 시 여기에 등록
            Node(
                  package='robot',           # 패키지 이름 (setup.py의 package_name)
                  executable='heartbeat',    # 실행 파일 이름 (setup.py의 entry_points)
                  name='heartbeat_node',     # ROS 2 네트워크에서 사용할 노드 이름 (super().__init__("camera_node")와 동일)
                  output='screen',           # 로그를 터미널에 출력
            ),
            Node(
                  package='robot',
                  executable='text_publisher',
                  name='text_publisher_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='text_subscriber',
                  name='text_subscriber_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='image_publisher',
                  name='image_publisher_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='image_subscriber',
                  name='image_subscriber_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='camera_publisher',
                  name='camera_publisher_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='camera_subscriber',
                  name='camera_subscriber_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='custom_message_type_publisher',
                  name='custom_message_type_publisher_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='led_server',
                  name='led_server_node',
                  output='screen',
            ),
            Node(
                  package='robot',
                  executable='led_server_with_custom_type',
                  name='led_server_node_with_custom_type',
                  output='screen',
            ),
    ])
