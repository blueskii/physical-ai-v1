import os

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraPublisherNode(Node):
    """
    MP4 영상 파일에서 프레임을 읽어 ROS2 Image 토픽으로 발행하는 노드.
    Topic: /camera/image_raw
    """

    def __init__(self):
        super().__init__('camera_publisher')

        self.declare_parameter('video_path', 'video/lane-seg.mp4')
        self.declare_parameter('publish_rate', 30.0)  # Hz
        self.declare_parameter('loop', True)          # EOF 시 처음부터 반복

        video_path   = str(self.get_parameter('video_path').value).strip()
        publish_rate = self.get_parameter('publish_rate').value
        self._loop   = self.get_parameter('loop').value

        # 상대 경로인 경우 현재 작업 디렉터리(워크스페이스 루트) 기준으로 절대 경로 변환
        if not os.path.isabs(video_path):
            video_path = os.path.normpath(os.path.join(os.getcwd(), video_path))

        if not os.path.isfile(video_path):
            self.get_logger().error(f'비디오 파일을 찾을 수 없습니다: {video_path}')
            raise RuntimeError(f'Video file not found: {video_path}')

        self._bridge = CvBridge()
        self._cap = cv2.VideoCapture(video_path)

        if not self._cap.isOpened():
            self.get_logger().error(f'비디오 파일을 열 수 없습니다: {video_path}')
            raise RuntimeError(f'Cannot open video file: {video_path}')

        total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        src_fps      = self._cap.get(cv2.CAP_PROP_FPS) or publish_rate

        self._publisher = self.create_publisher(Image, '/camera/image_raw', 10)

        period = 1.0 / publish_rate
        self._timer = self.create_timer(period, self._timer_callback)

        self.get_logger().info(
            f'CameraPublisher 시작 — 파일={video_path}, '
            f'원본FPS={src_fps:.1f}, 발행FPS={publish_rate:.1f}, '
            f'총프레임={total_frames}, 루프={self._loop}'
        )

    def _timer_callback(self):
        ret, frame = self._cap.read()
        if not ret:
            if self._loop:
                self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self._cap.read()
            if not ret:
                self.get_logger().warn('프레임 읽기 실패 또는 영상 끝.')
                return

        msg = self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'
        self._publisher.publish(msg)

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
        rclpy.shutdown()


if __name__ == '__main__':
    main()
