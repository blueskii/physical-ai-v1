import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher')

        self.declare_parameter('device_id', 0)
        self.declare_parameter('fps', 25.0)
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)

        device_id = self.get_parameter('device_id').get_parameter_value().integer_value
        fps = self.get_parameter('fps').get_parameter_value().double_value
        width = self.get_parameter('width').get_parameter_value().integer_value
        height = self.get_parameter('height').get_parameter_value().integer_value

        self._bridge = CvBridge()
        self._count = 0

        self._cap = cv2.VideoCapture(device_id, cv2.CAP_V4L2)
        if not self._cap.isOpened():
            self.get_logger().error(f'카메라 장치 {device_id}를 열 수 없습니다.')
            raise RuntimeError(f'Cannot open camera device {device_id}')

        self._cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._cap.set(cv2.CAP_PROP_FPS, fps)

        # Discard initial frames while the sensor warms up
        for _ in range(10):
            self._cap.read()

        actual_w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self._publisher = self.create_publisher(Image, '/topic/camera', 1)
        self._timer = self.create_timer(1.0 / fps, self._timer_callback)
        self.get_logger().info(
            f'Camera Publisher Started. device={device_id}, '
            f'해상도={actual_w}x{actual_h}, fps={fps}'
        )

    def _timer_callback(self):
        ret, frame = self._cap.read()
        if not ret:
            self.get_logger().warn('카메라 프레임 캡처 실패.')
            return

        self._count += 1
        msg = self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera'
        self._publisher.publish(msg)
        self.get_logger().debug(f'프레임 발행({self._count})')

    def destroy_node(self):
        if self._cap.isOpened():
            self._cap.release()
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
