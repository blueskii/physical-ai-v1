import threading

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class CameraSubscriberNode(Node):
    """
    /camera/image_raw 토픽을 구독하여 OpenCV GUI 창으로 실시간 재생하는 노드.

    ROS2 spin은 별도 스레드에서 실행하고,
    OpenCV GUI 루프(imshow/waitKey)는 반드시 메인 스레드에서 실행합니다.
    GUI 창을 닫거나 'q' 키를 누르면 노드가 종료됩니다.
    """

    def __init__(self):
        super().__init__('camera_subscriber')

        self.declare_parameter('window_name', 'Camera Feed')
        self.declare_parameter('window_width',  0)   # 0 = 원본 크기
        self.declare_parameter('window_height', 0)

        self._window_name   = self.get_parameter('window_name').value
        self._window_width  = self.get_parameter('window_width').value
        self._window_height = self.get_parameter('window_height').value

        self._bridge = CvBridge()
        self._frame_lock = threading.Lock()
        self._latest_frame: np.ndarray | None = None

        self._subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self._image_callback,
            10,
        )

        self.get_logger().info(
            f'CameraSubscriber 시작 — 토픽: /camera/image_raw, '
            f'창: "{self._window_name}"'
        )

    def _image_callback(self, msg: Image):
        """토픽에서 Image 메시지를 받아 OpenCV 프레임으로 변환 후 저장."""
        try:
            frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'imgmsg_to_cv2 실패: {e}')
            return

        with self._frame_lock:
            self._latest_frame = frame

    def get_latest_frame(self) -> np.ndarray | None:
        with self._frame_lock:
            return self._latest_frame.copy() if self._latest_frame is not None else None


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriberNode()

    window_name   = node._window_name
    window_width  = node._window_width
    window_height = node._window_height

    # ROS2 spin을 별도 스레드에서 실행 (GUI는 메인 스레드 전용)
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # 창을 즉시 표시하기 위해 빈 프레임으로 초기화
    placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(placeholder, 'Waiting for frames...', (120, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)
    cv2.imshow(window_name, placeholder)
    cv2.waitKey(1)

    window_shown = True  # imshow가 최소 한 번 호출됐는지 추적

    try:
        while rclpy.ok():
            frame = node.get_latest_frame()

            if frame is not None:
                if window_width > 0 and window_height > 0:
                    frame = cv2.resize(
                        frame,
                        (window_width, window_height),
                        interpolation=cv2.INTER_LINEAR,
                    )
                cv2.imshow(window_name, frame)

            # waitKey는 항상 호출해야 창이 응답함 (1ms 대기)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                node.get_logger().info("'q' 입력 — 종료합니다.")
                break

            # 창이 닫혔는지 확인 (imshow 이후부터만 체크)
            if window_shown and cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                node.get_logger().info('GUI 창이 닫혔습니다 — 종료합니다.')
                break

    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join(timeout=2.0)


if __name__ == '__main__':
    main()
