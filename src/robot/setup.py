import os                                       # 운영체제 관련 기능 (파일 경로 처리 등)
from glob import glob                           # launch 파일 경로 패턴 검색
from setuptools import find_packages, setup     # 패키지 자동 탐색 및 빌드 설정

package_name = 'robot'  # ROS 2 패키지 이름 (폴더명과 일치해야 함)

setup(
    name=package_name,      # 배포 패키지 이름
    version='0.0.1',        # 패키지 버전
    packages=find_packages(),   # __init__.py가 있는 모든 폴더를 패키지로 자동 탐색
    data_files=[
        # ROS 2 패키지 인덱스에 이 패키지를 등록 (ros2 pkg list에 표시되려면 필요)
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # package.xml을 share 디렉터리에 설치 (패키지 메타 정보)
        ('share/' + package_name, ['package.xml']),
        # launch 폴더의 모든 .py 파일을 share에 설치 (ros2 launch 명령으로 접근 가능)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],    # 빌드에 필요한 의존 패키지
    zip_safe=True,                      # zip 압축 배포 허용 여부
    maintainer='Your Name',             # 패키지 관리자 이름
    maintainer_email='your@email.com',  # 패키지 관리자 이메일
    description='Robot ROS 2 Package',  # 패키지 설명
    license='Apache-2.0',               # 라이선스
    entry_points={
        # ros2 run / ros2 launch 에서 실행할 수 있는 CLI 명령어 등록
        # 형식: '실행파일명 = 패키지.모듈:진입함수'
        'console_scripts': [
            # 새 노드 추가 시 여기에 등록
            # executable = package_name.module_name:main
            'heartbeat = robot.node.heartbeat_node:main',
            'text_publisher = robot.topic.text_publisher_node:main',
            'text_subscriber = robot.topic.text_subscriber_node:main',
            'image_publisher = robot.topic.image_publisher_node:main',
            'image_subscriber = robot.topic.image_subscriber_node:main',
            'camera_publisher = robot.topic.camera_publisher_node:main',
            'camera_subscriber = robot.topic.camera_subscriber_node:main',
            'custom_message_publisher = robot.topic.custom_message_publisher_node:main',
            'custom_message_subscriber = robot.topic.custom_message_subscriber_node:main',
            'led_server = robot.service.led_server_node:main',
            'led_client = robot.service.led_client_node:main',
            'led_server_with_custom_type = robot.service.led_server_node_with_custom_type:main',
            'led_client_with_custom_type = robot.service.led_client_node_with_custom_type:main',
            'move_server = robot.action.move_server_node:main',
            'move_client = robot.action.move_client_node:main',
            'param = robot.parameter.param_node:main',
        ],
    },
)
