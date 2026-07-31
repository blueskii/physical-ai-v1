import rclpy                      # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node       # 노드 기반 클래스
from std_msgs.msg import String   # 문자열 메시지 타입


class TextPublisherNode(Node):
    def __init__(self):
        super().__init__('text_publisher')             # 노드 이름 등록
        self._count = 0                                # 발행 횟수 카운터
        self._publisher = self.create_publisher(
            String,          # 메시지 타입
            '/topic/text',   # 토픽 이름
            1                # 큐 크기: 처리되지 않은 메시지를 최대 1개까지 버퍼링
        )
        self._timer = self.create_timer(1.0, self._timer_callback)  # 1초마다 콜백 호출
        self.get_logger().info('Text Publisher Started.')

    def _timer_callback(self):
        self._count += 1
        msg = String()                          # 메시지 객체 생성
        msg.data = f'텍스트({self._count})'    # 메시지 내용 설정
        self._publisher.publish(msg)            # 토픽에 발행
        self.get_logger().info(f'발행: {msg.data}')


def main(args=None):
    rclpy.init(args=args)          # ROS 2 초기화
    node = TextPublisherNode()
    try:
        rclpy.spin(node)           # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                       # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()        # 노드 자원 해제
        if rclpy.ok():
            rclpy.shutdown()       # ROS 2 종료
