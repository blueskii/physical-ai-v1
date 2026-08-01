import rclpy                                      # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                       # ROS 2 노드 기본 클래스
from robot_interfaces.msg import TextImage        # 텍스트 + 이미지 커스텀 메시지 타입
from cv_bridge import CvBridge                    # OpenCV 이미지 ↔ ROS 2 메시지 변환
import cv2                                        # 이미지 처리
import numpy as np                                # 배열 생성 (이미지 초기화)


class CustomMessageTypePublisherNode(Node):
    def __init__(self):
        # Node 초기화 및 노드 이름 등록
        super().__init__('custom_message_type_publisher_node')

        # OpenCV ↔ ROS 2 메시지 변환 객체
        self._bridge = CvBridge()

        # 총 발행 횟수
        self._count = 0

        # 테스트용 OpenCV 이미지 생성 (640x480 파란색 배경)
        # np.full: 모든 픽셀을 BGR [255, 100, 0] (파란색)으로 채운 배열 생성
        self._frame = cv2.rectangle(
            # BGR 파란색 배경
            np.full((480, 640, 3), [255, 100, 0], dtype=np.uint8),
            # 초록 테두리: 좌상단(50,100) ~ 우하단(590,430), 두께 5
            (50, 100), (590, 430), (0, 255, 0), 5
        )

        # 퍼블리셔 생성: TextImage 메시지를 /topic/text_image 토픽에 발행
        self._publisher = self.create_publisher(
            TextImage,              # 커스텀 메시지 타입
            '/topic/text_image',    # 토픽 이름
            1                       # 큐 크기 (최신 메시지 1개만 유지)
        )

        # 1초마다 _timer_callback 호출하도록 타이머 생성
        self._timer = self.create_timer(1.0, self._timer_callback)
        self.get_logger().info('Custom Message Type Publisher Node started.')

    def _timer_callback(self):
        # 커스텀 메시지 객체 생성
        msg = TextImage()

        # text 필드 설정
        self._count += 1
        msg.text = f'Text Message ({self._count})'

        # image 필드 설정
        # OpenCV BGR 이미지 → ROS 2 Image 메시지 변환
        msg.image = self._bridge.cv2_to_imgmsg(self._frame, encoding='bgr8')
        # 발행 시각 기록 (ROS 2 Time → Header stamp)
        msg.image.header.stamp = self.get_clock().now().to_msg()

        # 토픽에 발행
        self._publisher.publish(msg)
        self.get_logger().info(f'발행({self._count})')


def main(args=None):
    rclpy.init(args=args)                   # ROS 2 초기화
    node = CustomMessageTypePublisherNode() # 노드 생성
    try:
        rclpy.spin(node)                    # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                                # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()                 # 노드 자원 해제
        if rclpy.ok():                      # ROS 2 런타임이 현재 정상 동작 중인지 확인
            rclpy.shutdown()                # ROS 2 종료
