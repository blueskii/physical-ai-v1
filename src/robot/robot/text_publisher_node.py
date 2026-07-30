import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TextPublisherNode(Node):
    def __init__(self):
        super().__init__('text_publisher')
        self._count = 0
        self._publisher = self.create_publisher(String, '/topic/text', 1)
        self._timer = self.create_timer(1.0, self._timer_callback)
        self.get_logger().info('Text Publisher Started.')

    def _timer_callback(self):
        self._count += 1
        msg = String()
        msg.data = f'텍스트({self._count})'
        self._publisher.publish(msg)
        self.get_logger().info(f'발행: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = TextPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
