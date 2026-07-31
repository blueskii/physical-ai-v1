import rclpy                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node         # 노드 기반 클래스
from sensor_msgs.msg import Image   # ROS 2 이미지 메시지 타입
from cv_bridge import CvBridge      # OpenCV 이미지 ↔ ROS 2 메시지 변환
import cv2                          # 카메라 캡처 및 이미지 처리


class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher')    # 노드 이름 등록

        # 외부에서 오버라이드 가능한 파라미터 선언 (기본값 설정)
        # 예) ros2 run robot camera_publisher_node --ros-args -p device_id:=1 -p fps:=30.0
        self.declare_parameter('device_id', 0)      # 카메라 장치 번호 (/dev/video0)
        self.declare_parameter('fps', 25.0)          # 초당 프레임 수
        self.declare_parameter('width', 640)         # 프레임 가로 해상도
        self.declare_parameter('height', 480)        # 프레임 세로 해상도

        # 선언된 파라미터 값 읽기
        device_id = self.get_parameter('device_id').get_parameter_value().integer_value
        fps       = self.get_parameter('fps').get_parameter_value().double_value
        width     = self.get_parameter('width').get_parameter_value().integer_value
        height    = self.get_parameter('height').get_parameter_value().integer_value

        self._bridge = CvBridge()   # OpenCV ↔ ROS 2 메시지 변환 객체
        self._count = 0             # 총 발행 횟수

        # V4L2 드라이버로 카메라 장치 열기
        self._cap = cv2.VideoCapture(device_id, cv2.CAP_V4L2)
        if not self._cap.isOpened():
            self.get_logger().error(f'카메라 장치 {device_id}를 열 수 없습니다.')
            raise RuntimeError(f'Cannot open camera device {device_id}')

        # 카메라 속성 설정 (MJPG 포맷으로 고해상도/고fps 지원)
        self._cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._cap.set(cv2.CAP_PROP_FPS, fps)

        # 센서 워밍업: 초기 프레임 10장 버림 (불안정한 초기 프레임 제거)
        for _ in range(10):
            self._cap.read()

        # 실제 적용된 해상도 확인 (요청값과 다를 수 있음)
        actual_w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self._publisher = self.create_publisher(Image, '/topic/camera', 1)
        self._timer = self.create_timer(1.0 / fps, self._timer_callback)  # fps 주기로 콜백 호출
        self.get_logger().info(
            f'Camera Publisher Started. device={device_id}, '
            f'해상도={actual_w}x{actual_h}, fps={fps}'
        )

    def _timer_callback(self):
        ret, frame = self._cap.read()   # 카메라에서 프레임 1장 캡처
        if not ret:
            self.get_logger().warn('카메라 프레임 캡처 실패.')
            return

        self._count += 1
        # OpenCV 이미지를 ROS 2 Image 메시지로 변환
        msg = self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()  # 캡처 시각 기록
        msg.header.frame_id = 'camera'                      # 프레임 ID (좌표계 식별자)
        self._publisher.publish(msg)                        # 토픽에 발행
        self.get_logger().debug(f'프레임 발행({self._count})')

    def destroy_node(self):
        if self._cap.isOpened():
            self._cap.release()     # 카메라 장치 해제
        super().destroy_node()      # 부모 클래스의 자원 해제


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = CameraPublisherNode()
    try:
        rclpy.spin(node)            # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()        # ROS 2 종료
