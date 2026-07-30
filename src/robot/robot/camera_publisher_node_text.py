import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self._count = 0
        self._publisher = self.create_publisher(String, '/camera/image_raw', 10)
        self._timer = self.create_timer(1.0, self._timer_callback)
        self.get_logger().info('Camera Publisher Started.')

    def _timer_callback(self):
        self._count += 1
        msg = String()
        msg.data = f'이미지({self._count})'
        self._publisher.publish(msg)
        self.get_logger().info(f'발행: {msg.data}')


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
