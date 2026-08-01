import rclpy                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node         # 노드 기반 클래스
from sensor_msgs.msg import Image   # ROS 2 이미지 메시지 타입
from cv_bridge import CvBridge      # OpenCV 이미지 ↔ ROS 2 메시지 변환
import cv2                          # 이미지 표시 및 처리


class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber')   # 노드 이름 등록
        self._bridge = CvBridge()               # OpenCV ↔ ROS 2 메시지 변환 객체
        self._latest_frame = None               # 가장 최근에 수신한 프레임 (없으면 None)
        self._subscription = self.create_subscription(
            Image,              # 구독할 메시지 타입
            '/topic/camera',    # 구독할 토픽 이름
            self._callback,     # 메시지 수신 시 호출할 콜백 함수
            1                   # QoS 큐 크기 (최신 프레임 1장만 유지)
        )

    def _callback(self, msg: Image):
        # ROS 2 Image 메시지를 OpenCV BGR 이미지로 변환하여 저장
        self._latest_frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


def main(args=None):
    rclpy.init(args=args)                                       # ROS 2 초기화
    node = CameraSubscriberNode()
    cv2.namedWindow('camera_subscriber', cv2.WINDOW_NORMAL)    # 리사이즈 가능한 창 생성
    try:
        while rclpy.ok():
            # 콜백 1회 처리 (발행된 메시지가 있으면 1번 콜백 처리, 없으면 최대 10ms 대기하고 콜백 호출 없이 리턴)
            rclpy.spin_once(node, timeout_sec=0.01)
            # 최신 프레임이 있으면 OpenCV 창에 표시
            if node._latest_frame is not None:
                # 최신 프레임을 렌더링 버퍼에 저장 (실제 표시는 waitKey에서)  
                cv2.imshow('camera_subscriber', node._latest_frame)          
            # cv2.waitKey(1): GUI 이벤트 루프 실행 + 창 렌더링 (imshow 단독으로는 화면에 표시 안 됨)
            if cv2.waitKey(1) == ord('q'):  # 'q' 키 입력 시 루프 종료
                break
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        cv2.destroyAllWindows()     # 모든 OpenCV 창 닫기
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():              # ROS 2 런타임이 현재 정상 동작 중인지 확인 
            rclpy.shutdown()        # ROS 2 종료
