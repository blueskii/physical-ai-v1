import rclpy                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node         # 노드 기반 클래스
from sensor_msgs.msg import Image   # ROS 2 이미지 메시지 타입
from cv_bridge import CvBridge      # ROS 2 메시지 ↔ OpenCV 이미지 변환
import cv2                          # 이미지 화면 출력


class ImageSubscriberNode(Node):
    def __init__(self):
        super().__init__('image_subscriber')    # 노드 이름 등록
        self._bridge = CvBridge()               # ROS 2 메시지 ↔ OpenCV 변환 객체
        self._latest_frame = None               # 가장 최근에 수신한 OpenCV 이미지
        self._count = 0                         # 총 수신 횟수
        self._subscription = self.create_subscription(
            Image,           # 메시지 타입
            '/topic/image',  # 구독할 토픽 이름
            self._callback,  # 메시지 수신 시 호출할 콜백 함수
            1                # 큐 크기
        )
        self.get_logger().info('Image Subscriber Started.')

    def _callback(self, msg: Image):
        self._count += 1
        # ROS 2 이미지 메시지를 OpenCV 이미지(BGR)로 변환해서 저장
        self._latest_frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.get_logger().info(f'구독({self._count}): image')


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = ImageSubscriberNode()
    cv2.namedWindow('image_subscriber', cv2.WINDOW_NORMAL)  # 표시할 윈도우 생성
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)  # 콜백 한 번 처리 후 반환 (최대 0.01초 대기)
            if node._latest_frame is not None:
                cv2.imshow('image_subscriber', node._latest_frame)  # 최신 프레임 화면에 표시
            if cv2.waitKey(1) == ord('q'):  # q 키 입력 시 종료
                break
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        cv2.destroyAllWindows()     # 열린 OpenCV 윈도우 모두 닫기
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()        # ROS 2 종료

