import rclpy                                        # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                         # 노드 기반 클래스
from rcl_interfaces.msg import SetParametersResult  # 파라미터 변경 결과 메시지

# ROS 2 Parameter 예제 노드
class ParamNode(Node):
    # 노드 초기화 메소드
    def __init__(self):
        super().__init__('param_node')  # 노드 이름 등록

        # 파라미터 선언 
        # - declare_parameter(이름, 기본값)
        # - 기본값의 타입이 파라미터 타입으로 자동 결정
        self.declare_parameter('robot_name', 'MyRobot')   # str
        self.declare_parameter('timer_period', 1.0)       # float  (초)
        self.declare_parameter('max_speed', 1.5)          # float  (m/s)
        self.declare_parameter('debug_mode', False)       # bool

        # 파라미터 값 읽기
        robot_name   = self.get_parameter('robot_name').value
        timer_period = self.get_parameter('timer_period').value
        self.get_logger().info(f'[초기값] robot_name={robot_name}, timer_period={timer_period}s')

        # 파라미터 변경 콜백 등록
        # - ros2 param set 명령 등으로 파라미터가 변경될 때 자동 호출됩니다.
        self.add_on_set_parameters_callback(self._on_params_changed)

        # 타이머: timer_period 파라미터에 따라 주기를 동적 변경
        self._timer = self.create_timer(timer_period, self._timer_callback)
        self.get_logger().info('Parameter Node Started. (Ctrl+C 로 종료)')
        
    # 파라미터 변경 콜백
    def _on_params_changed(self, params):
        """
        파라미터가 변경될 때마다 호출
        params 는 이번에 변경된 파라미터들의 리스트
        param.name 으로 어떤 파라미터가 바뀌었는지 정확히 식별할 수 있음
        """
        for param in params:
            self.get_logger().info(f'[파라미터 변경] {param.name} = {param.value}')

            if param.name == 'robot_name':
                # robot_name 이 변경된 경우
                self.get_logger().info(f'로봇 이름이 "{param.value}" 으로 변경됐습니다.')

            elif param.name == 'timer_period':
                # timer_period 가 변경된 경우 → 타이머 주기를 실시간으로 갱신
                if param.value <= 0:
                    self.get_logger().warn('timer_period 는 0보다 커야 합니다. 무시합니다.')
                    return SetParametersResult(successful=False)
                self._timer.cancel()
                self._timer = self.create_timer(param.value, self._timer_callback)
                self.get_logger().info(f'타이머 주기가 {param.value}s 로 변경됐습니다.')

            elif param.name == 'max_speed':
                # max_speed 가 변경된 경우
                self.get_logger().info(f'최대 속도가 {param.value:.1f} m/s 로 변경됐습니다.')

            elif param.name == 'debug_mode':
                # debug_mode 가 변경된 경우
                state = '활성화' if param.value else '비활성화'
                self.get_logger().info(f'디버그 모드가 {state}됐습니다.')

        # successful=True 를 반환해야 변경이 실제로 적용됩니다.
        return SetParametersResult(successful=True)        

    # 타이머 콜백
    def _timer_callback(self):
        name      = self.get_parameter('robot_name').value
        max_speed = self.get_parameter('max_speed').value
        debug     = self.get_parameter('debug_mode').value
        self.get_logger().info(
            f'robot_name={name} | max_speed={max_speed:.1f} m/s | debug={debug}'
        )


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = ParamNode()              # 노드 생성
    try:
        rclpy.spin(node)            # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():              # ROS 2가 정상적으로 초기화된 상태라면 종료
            rclpy.shutdown()        # ROS 2 종료
