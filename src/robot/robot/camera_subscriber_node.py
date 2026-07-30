import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self._bridge = CvBridge()
        self._latest_frame = None
        self._count = 0
        self._subscription = self.create_subscription(
            Image,
            '/topic/camera',
            self._callback,
            1
        )

    def _callback(self, msg: Image):
        self._count += 1
        self._latest_frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriberNode()
    cv2.namedWindow('camera_subscriber', cv2.WINDOW_NORMAL)
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)
            if node._latest_frame is not None:
                cv2.imshow('camera_subscriber', node._latest_frame)
            if cv2.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
