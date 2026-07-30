import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher')

        image_path = os.path.join(os.getcwd(), 'video/image1.png')
        frame = cv2.imread(image_path)
        if frame is None:
            self.get_logger().error(f'이미지 파일을 열 수 없습니다: {image_path}')
            raise RuntimeError(f'Cannot open image: {image_path}')

        self._bridge = CvBridge()
        self._msg = self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')

        self._count = 0
        self._publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self._timer = self.create_timer(1.0, self._timer_callback)
        self.get_logger().info(f'Camera Publisher Started. 이미지={image_path}')

    def _timer_callback(self):
        self._count += 1
        self._msg.header.stamp = self.get_clock().now().to_msg()
        self._publisher.publish(self._msg)
        self.get_logger().info(f'발행({self._count}): image1.png')


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


if __name__ == '__main__':
    main()
