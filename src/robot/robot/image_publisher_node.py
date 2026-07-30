import os
import glob
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher')

        images_dir = os.path.join(os.getcwd(), 'data/images')
        paths = sorted(glob.glob(os.path.join(images_dir, '*.png')))

        self._bridge = CvBridge()
        self._frames = []
        for p in paths:
            frame = cv2.imread(p)
            if frame is not None:
                self._frames.append((os.path.basename(p), self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')))

        self._index = 0
        self._count = 0
        self._publisher = self.create_publisher(Image, '/topic/image', 1)
        self._timer = self.create_timer(1.0/25, self._timer_callback)
        self.get_logger().info(f'Image Publisher Started. 이미지 {len(self._frames)}장 로드.')

    def _timer_callback(self):
        self._count += 1
        name, msg = self._frames[self._index]
        msg.header.stamp = self.get_clock().now().to_msg()
        self._publisher.publish(msg)
        self.get_logger().info(f'발행({self._count}): {name}')
        self._index = (self._index + 1) % len(self._frames)


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
