import rclpy                                      # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                       # ROS 2 노드 기본 클래스
from robot_interfaces.msg import TextImage        # 텍스트 + 이미지 커스텀 메시지 타입
from cv_bridge import CvBridge                    # ROS 2 메시지 ↔ OpenCV 이미지 변환
import cv2                                        # 이미지 화면 출력


class CustomMessageTypeSubscriberNode(Node):
    def __init__(self):
        # Node 초기화 및 노드 이름 등록
        super().__init__('custom_message_type_subscriber_node')

        self._bridge = CvBridge()               # ROS 2 메시지 ↔ OpenCV 변환 객체
        self._latest_frame = None               # 가장 최근에 수신한 OpenCV 이미지
        self._latest_text = ''                  # 가장 최근에 수신한 텍스트

        # 구독자 생성
        self._subscription = self.create_subscription(
            TextImage,              # 커스텀 메시지 타입 (서버와 동일해야 함)
            '/topic/text_image',    # 구독할 토픽 이름
            self._callback,         # 메시지 수신 시 호출할 콜백 함수
            1                       # 큐 크기
        )
        self.get_logger().info('Custom Message Type Subscriber Node started.')

    def _callback(self, msg: TextImage):
        # 텍스트 필드 저장
        self._latest_text = msg.text
        # 이미지 필드 변환 후 저장
        self._latest_frame = self._bridge.imgmsg_to_cv2(msg.image, desired_encoding='bgr8')

        # 이미지에 텍스트 오버레이
        cv2.putText(
            self._latest_frame,
            self._latest_text,
            (30, 50),                   # 텍스트 출력 위치 (x, y)
            cv2.FONT_HERSHEY_SIMPLEX,   # 폰트
            1.0,                        # 폰트 크기
            (255, 255, 255),            # 텍스트 색상 (흰색)
            2                           # 텍스트 두께
        )
        self.get_logger().info(f'구독: {self._latest_text}')


def main(args=None):
    rclpy.init(args=args)                                                   # ROS 2 초기화
    node = CustomMessageTypeSubscriberNode()                                # 노드 생성
    cv2.namedWindow('custom_message_type_subscriber', cv2.WINDOW_NORMAL)    # 표시할 윈도우 생성
    try:
        while rclpy.ok():   # ROS 2 런타임이 현재 정상 동작 중인지 확인
            # 콜백 한 번 처리 후 반환 (최대 0.01초 대기)
            rclpy.spin_once(node, timeout_sec=0.01) 
            # 최신 프레임이 있으면 화면에 표시
            if node._latest_frame is not None:
                cv2.imshow('custom_message_type_subscriber', node._latest_frame)
            # cv2.waitKey(1): GUI 이벤트 루프 실행 + 창 렌더링 (imshow 단독으로는 화면에 표시 안 됨)
            if cv2.waitKey(1) == ord('q'):  # q 키 입력 시 종료
                break
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        cv2.destroyAllWindows()     # 열린 OpenCV 윈도우 모두 닫기
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():              # ROS 2 런타임이 현재 정상 동작 중인지 확인
            rclpy.shutdown()        # ROS 2 종료
