import os                           # 파일 경로 조합
import glob                         # 파일 경로 패턴 검색
import rclpy                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node         # 노드 기반 클래스
from sensor_msgs.msg import Image   # ROS 2 이미지 메시지 타입
from cv_bridge import CvBridge      # OpenCV 이미지 ↔ ROS 2 메시지 변환
import cv2                          # 이미지 파일 읽기


class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher')   # 노드 이름 등록

        # zdata/images 폴더에서 PNG 파일 목록을 정렬해서 로드
        images_dir = os.path.join(os.getcwd(), 'zdata/images')
        paths = sorted(glob.glob(os.path.join(images_dir, '*.png')))

        self._bridge = CvBridge()   # OpenCV ↔ ROS 2 메시지 변환 객체
        self._frames = []           # (파일명, ROS 이미지 메시지) 튜플 목록
        for p in paths:
            frame = cv2.imread(p)   # PNG 파일을 OpenCV 이미지로 읽기
            if frame is not None:
                # (파일명, ROS 이미지 메시지) 튜플로 변환해서 저장
                self._frames.append(
                    (os.path.basename(p), 
                    self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')))

        self._index = 0                # 현재 발행할 프레임 인덱스
        self._count = 0                # 총 발행 횟수
        self._publisher = self.create_publisher(Image, '/topic/image', 1)
        self._timer = self.create_timer(1.0/25, self._timer_callback)  # 25fps로 발행
        self.get_logger().info(f'Image Publisher Started. 이미지 {len(self._frames)}장 로드.')

    def _timer_callback(self):
        self._count += 1
        name, msg = self._frames[self._index]                       # 현재 프레임 가져오기
        msg.header.stamp = self.get_clock().now().to_msg()          # 현재 시각을 메시지 헤더에 기록
        self._publisher.publish(msg)                                # 토픽에 발행
        self.get_logger().info(f'발행({self._count}): {name}')
        self._index = (self._index + 1) % len(self._frames)        # 다음 프레임으로 순환


def main(args=None):
    rclpy.init(args=args)          # ROS 2 초기화
    node = ImagePublisherNode()
    try:
        rclpy.spin(node)           # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                       # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()        # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()       # ROS 2 종료
