import rclpy                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node         # ROS 2 노드 기본 클래스
from std_srvs.srv import SetBool    # LED ON/OFF 제어 서비스 타입 (request: bool, response: bool + string)
from std_srvs.srv import Trigger    # LED 상태 조회 서비스 타입 (request: 없음, response: bool + string)

# LED 제어 서비스 서버 노드
class LedServerNode(Node):
    def __init__(self):
        # 부모 초기화 메소드 호출: 노드 이름 등록
        super().__init__('led_server_node')

        self._led_state = False     # 현재 LED 상태 (False=OFF, True=ON)

        # LED 상태 변경 서비스 서버 생성
        self._set_service = self.create_service(
            SetBool,                # 서비스 타입
            '/service/led/set',     # 서비스 이름
            self._handle_set        # 요청 수신 시 호출할 콜백 함수
        )

        # LED 상태 조회 서비스 서버 생성
        self._get_service = self.create_service(
            Trigger,                # 서비스 타입
            '/service/led/get',     # 서비스 이름
            self._handle_get        # 요청 수신 시 호출할 콜백 함수
        )

        self.get_logger().info('LED 서비스 시작됨.')

   # LED 상태 변경 요청 처리 콜백
    def _handle_set(self, request: SetBool.Request, response: SetBool.Response):
        # 상태 변경 처리
        self._led_state = request.data

        # 처리 결과 로그 출력
        self.get_logger().info(f'LED 상태 변경 처리 -> {self._led_state}')

        # 응답 생성
        response.success = True
        response.message = "ON" if self._led_state else "OFF"
        return response

    def _handle_get(self, request: Trigger.Request, response: Trigger.Response):
        # 현재 상태 로그 출력
        self.get_logger().info(f'LED 상태 조회 처리: state={self._led_state}')

        # 응답 생성
        response.success = True
        response.message = "ON" if self._led_state else "OFF"
        return response


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = LedServerNode()          # LED 서비스 서버 노드 생성
    try:
        rclpy.spin(node)            # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()        # ROS 2 종료
