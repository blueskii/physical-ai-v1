import rclpy                    # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node     # ROS 2 노드 기본 클래스

# ROS 2 노드의 기본 단위인 Node 클래스를 상속받아 HeartbeatNode를 정의
class HeartbeatNode(Node):
    def __init__(self):
        # 부모 클래스(Node) 초기화, 'heartbeat'는 ROS 2 네트워크에서 사용할 노드 이름
        super().__init__('heartbeat_node')
        # 1.0초 주기로 timer_callback을 반복 호출하는 타이머 생성
        self.timer = self.create_timer(1.0, self.timer_callback)
        # 노드 시작 시 로그 출력 (INFO 레벨)
        self.get_logger().info('Heartbeat Node started')

    def timer_callback(self):
        # 1초마다 호출되어 노드가 살아있음을 로그로 기록
        self.get_logger().info('alive')

def main(args=None):
    # ROS Python 클라이언트 라이브러리 초기화
    rclpy.init(args=args)
    
    # HeartbeatNode 인스턴스 생성 → __init__ 실행
    node = HeartbeatNode()
    try:
        # 노드를 실행 상태로 유지하며 타이머 등의 콜백을 처리
        # - Ctrl+C 또는 외부 종료 신호가 올 때까지 블로킹
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C 입력 시 종료 메시지 출력
        pass
    finally:
        # Node 종료 후 정리
        node.destroy_node()
        # ROS Client Library 종료 (이미 종료된 경우 중복 호출 방지)
        if rclpy.ok():
            rclpy.shutdown()    