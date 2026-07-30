import os
from glob import glob
from setuptools import setup

package_name = 'robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='Robot ROS 2 Package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # 새 노드 추가 시 여기에 등록
            # executable = package_name.module_name:main
            'heartbeat = robot.heartbeat_node:main',
            'text_publisher = robot.text_publisher_node:main',
            'text_subscriber = robot.text_subscriber_node:main',
            'image_publisher = robot.image_publisher_node:main',
            'image_subscriber = robot.image_subscriber_node:main',
            'camera_publisher = robot.camera_publisher_node:main',
            'camera_subscriber = robot.camera_subscriber_node:main',
        ],
    },
)
