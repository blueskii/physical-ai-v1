import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self._subscription = self.create_subscription(
            String,
            '/camera/image_raw',
            self._callback,
            10
        )
        self.get_logger().info('Camera Subscriber Started.')

    def _callback(self, msg: String):
        self.get_logger().info(f'수신: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriberNode()
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
