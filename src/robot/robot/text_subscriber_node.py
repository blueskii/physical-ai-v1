import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TextSubscriberNode(Node):
    def __init__(self):
        super().__init__('text_subscriber')
        self._subscription = self.create_subscription(
            String,
            '/topic/text',
            self._callback,
            1
        )
        self.get_logger().info('Text Subscriber Started.')

    def _callback(self, msg: String):
        self.get_logger().info(f'수신: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = TextSubscriberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
