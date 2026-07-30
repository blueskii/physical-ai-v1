from launch import LaunchDescription
from launch_ros.actions import Node

# 런치 명세(LaunchDescription)를 반환하는 함수
# - ROS 2 launch 시스템이 이 함수를 호출해서 어떤 노드를 어떤 설정으로 실행할지 파악
def generate_launch_description():
    return LaunchDescription([
            새 노드 추가 시 여기에 등록
            Node(
                  package='robot',
                  executable='heartbeat',
                  name='heartbeat_node',
                  output='screen',
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
    ])
