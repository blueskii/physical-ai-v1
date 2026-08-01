import rclpy                                      # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                       # ROS 2 노드 기본 클래스
from robot_interfaces.srv import LedSet           # LED 제어 커스텀 서비스 타입 (state + brightness)
from robot_interfaces.srv import LedGet           # LED 상태 조회 커스텀 서비스 타입

# LED 제어 서비스 서버 노드
class LedServerNodeWithCustomType(Node):
    def __init__(self):
        # 부모 초기화 메소드 호출: 노드 이름 등록
        super().__init__('led_server_node_with_custom_type')

        self._led_state = False                     # 현재 LED 상태 (False=OFF, True=ON)
        self._led_brightness = 0                    # 현재 LED 밝기 (0-255)

        # LED 상태 변경 서비스 서버 생성
        self._set_service = self.create_service(
            LedSet,                                 # 서비스 타입
            '/service/led/set_with_custom_type',    # 서비스 이름
            self._handle_set                        # 요청 수신 시 호출할 콜백 함수
        )

        # LED 상태 조회 서비스 서버 생성
        self._get_service = self.create_service(
            LedGet,                                 # 서비스 타입
            '/service/led/get_with_custom_type',    # 서비스 이름
            self._handle_get                        # 요청 수신 시 호출할 콜백 함수
        )

        self.get_logger().info('LED 서비스 시작됨.')

    # LED 상태 변경 요청 처리 콜백
    def _handle_set(self, request: LedSet.Request, response: LedSet.Response):
        # 상태 변경 처리
        self._led_state = request.state             
        self._led_brightness = request.brightness   

        # 처리 결과 로그 출력      
        self.get_logger().info(
            f'LED 상태 변경 처리: state={self._led_state}, brightness={self._led_brightness}'
        )

        # 응답 생성
        response.success = True
        response.state = self._led_state
        response.brightness = self._led_brightness
        return response

    def _handle_get(self, request: LedGet.Request, response: LedGet.Response):
        # 현재 상태 로그 출력
        self.get_logger().info(
            f'LED 상태 조회 처리: state={self._led_state}, brightness={self._led_brightness}'
        )

        # 응답 생성
        response.success = True
        response.state = self._led_state
        response.brightness = self._led_brightness
        return response


def main(args=None):
    rclpy.init(args=args)                   # ROS 2 초기화
    node = LedServerNodeWithCustomType()    # 노드 생성
    try:
        rclpy.spin(node)                    # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                                # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()                 # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()                # ROS 2 종료
