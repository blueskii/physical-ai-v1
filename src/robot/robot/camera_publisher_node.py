import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge


class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__("camera_publisher_node")

        # Image 메시지를 '/camera/image_raw' 토픽으로 발행하는 Publisher 생성
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)

        # OpenCV와 ROS Image 메시지 간 변환을 위한 CvBridge
        self.bridge = CvBridge()

        # 카메라 열기 (0: 기본 카메라)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open camera.")

        # 0.1초(10Hz) 주기로 프레임 캡처 및 발행
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info("Camera Publisher Node Started.")

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Failed to capture frame.")
            return

        # OpenCV BGR 이미지를 ROS Image 메시지로 변환 후 발행
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'
        self.publisher_.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
