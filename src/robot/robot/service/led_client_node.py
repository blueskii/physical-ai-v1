import rclpy                              # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node               # ROS 2 노드 기본 클래스
from std_srvs.srv import SetBool          # LED ON/OFF 제어 서비스 타입
from std_srvs.srv import Trigger          # LED 상태 조회 서비스 타입

# LED 제어 서비스 클라이언트 노드
class LedClientNode(Node):
    # 부모 초기화 메소드 호출: 노드 이름 등록
    def __init__(self):
        super().__init__('led_client_node')

        # LED 상태 변경 서비스 클라이언트 생성
        self._set_client = self.create_client(
            SetBool,                # 서비스 타입 (서버와 동일해야 함)
            '/service/led/set'      # 서비스 이름 (서버와 동일해야 함)
        )

         # LED 상태 조회 서비스 클라이언트 생성
        self._get_client = self.create_client(
            Trigger,                # 서비스 타입 (서버와 동일해야 함)
            '/service/led/get'      # 서비스 이름 (서버와 동일해야 함)
        )

    # 서비스 서버가 준비될 때까지 대기 (서버가 아직 실행되지 않은 경우 대비)
    def _wait_for_server(self):
        self.get_logger().info('LED 서비스 연결 대기 중...')
        self._set_client.wait_for_service()
        self._get_client.wait_for_service()
        self.get_logger().info('LED 서비스 연결 완료.')

    # LED 상태 변경 요청
    def set_led(self, state: bool) -> str:
        # 요청 생성
        request = SetBool.Request()
        request.data = state 

        # 서버에 요청을 보내고 응답이 올 때까지 블로킹
        future = self._set_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        # 응답 처리
        response = future.result()
        return f'state={response.success}, message={response.message}'

    # LED 상태 조회 요청
    def get_led(self) -> str:
        # 요청 생성 (요청 파라미터 없음)
        request = Trigger.Request()

        # 서버에 요청을 보내고 응답이 올 때까지 블로킹
        future = self._get_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        # 응답 처리
        response = future.result()
        return f'state={response.success}, message={response.message}'


def main(args=None):
    # ROS 2 초기화    
    rclpy.init(args=args)

    # 노드 생성
    node = LedClientNode()

    # 서비스 서버가 준비될 때까지 대기
    node._wait_for_server()

    # --- 테스트 시작 ---

    # 1. LED 상태 변경 요청
    result = node.set_led(True)
    node.get_logger().info(f'LED 상태 변경 요청: {result}')

    # 2. 상태 조회
    result = node.get_led()
    node.get_logger().info(f'LED 상태 조회 요청: {result}')

    # --- 테스트 완료 ---

    node.destroy_node()     # 노드 자원 해제
    if rclpy.ok():          # ROS 2 런타임이 현재 정상 동작 중인지 확인
        rclpy.shutdown()    # ROS 2 종료
