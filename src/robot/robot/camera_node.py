# ROS Client Library for Python 가져오기
import rclpy

# Node 클래스 가져오기
from rclpy.node import Node

# Node의 자식 클래스로 CameraNode 정의
class CameraNode(Node):
    def __init__(self):
        # 부모 클래스의 초기화
        super().__init__("camera_node")
        
        # 1.0초 주기로 timer_callback을 반복 호출하는 타이머 생성
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        # 로거를 사용하여 노드 시작 메시지 출력
        self.get_logger().info("Camera Node Started.")
        
    def timer_callback(self):
        # 1초마다 호출되어 노드가 살아있음을 로그로 기록
        self.get_logger().info('Camera Capturing')        
        
def main(args=None):
    # ROS Client Library 초기화
    rclpy.init(args=args)
    # CameraNode 인스턴스 생성
    node = CameraNode()
    try:
        # Node가 종료되지 않도록 계속 실행
        # 사용자가 Ctrl+C를 누르면 종료
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
