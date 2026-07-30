import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
import cv2


class CameraSubscriberNode(Node):
    """
    /camera/image_raw 토픽을 구독하여 수신된 프레임을 화면에 표시하는 노드.
    """

    def __init__(self):
        super().__init__('camera_subscriber')

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self._bridge = CvBridge()
        self._latest_frame = None

        # 노드 시작 즉시 창 생성
        cv2.namedWindow('camera_subscriber', cv2.WINDOW_NORMAL)

        self._subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self._image_callback,
            qos
        )

        self.get_logger().info('CameraSubscriber 시작 — /camera/image_raw 구독 중.')

    def _image_callback(self, msg: Image):
        self._latest_frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriberNode()
    try:
        # spin_once + cv2.waitKey 메인 루프:
        # ROS2 메시지 처리와 OpenCV GUI를 같은 스레드에서 직접 제어
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)
            if node._latest_frame is not None:
                cv2.imshow('camera_subscriber', node._latest_frame)
            if cv2.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
