import rclpy                      # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node       # 노드 기반 클래스
from std_msgs.msg import String   # 문자열 메시지 타입


class TextSubscriberNode(Node):
    def __init__(self):
        super().__init__('text_subscriber')            # 노드 이름 등록
        self._subscription = self.create_subscription(
            String,           # 메시지 타입
            '/topic/text',    # 구독할 토픽 이름
            self._callback,   # 메시지 수신 시 호출할 콜백 함수
            1                 # 큐 크기: 처리되지 않은 메시지를 최대 1개까지 버퍼링
        )
        self.get_logger().info('Text Subscriber Started.')

    def _callback(self, msg: String):
        self.get_logger().info(f'구독: {msg.data}')   # 수신한 메시지 출력


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = TextSubscriberNode()
    try:
        rclpy.spin(node)            # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():              # ROS 2 런타임이 현재 정상 동작 중인지 확인
            rclpy.shutdown()        # ROS 2 종료
