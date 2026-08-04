import rclpy                                          # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                           # ROS 2 노드 기본 클래스
from rclpy.action import ActionClient                 # 액션 클라이언트 클래스
from rclpy.action.client import ClientGoalHandle      # 목표 핸들 (취소 등에 사용)
from robot_interfaces.action import Move              # Move 액션 타입 (Goal/Result/Feedback)
import time                                           # 취소 요청 시 딜레이용
import threading                                      # 취소 요청 시 별도 스레드 사용

# Move 액션 클라이언트 노드
class MoveClientNode(Node):
    def __init__(self):
        # 부모 초기화 메소드 호출: 노드 이름 등록
        super().__init__('move_client_node')

        # Move 액션 클라이언트 생성
        self._action_client = ActionClient(
            self,               # 노드
            Move,               # 액션 타입 (서버와 동일해야 함)
            '/action/move'      # 액션 이름 (서버와 동일해야 함)
        )

    # 액션 서버가 준비될 때까지 대기
    def _wait_for_server(self):
        self.get_logger().info('Move 액션 서버 연결 대기 중...')
        self._action_client.wait_for_server()
        self.get_logger().info('Move 액션 서버 연결 완료.')

    # 피드백 수신 콜백
    def _on_feedback(self, feedback_msg):
        feedback: Move.Feedback = feedback_msg.feedback
        self.get_logger().info(
            f'피드백 수신: current={feedback.current_distance:.2f}, '
            f'progress={feedback.progress:.0%}'
        )

    # 이동 목표 전송
    def send_goal(self, distance: float):
        # 목표 생성
        goal = Move.Goal()
        goal.distance = distance

        # 서버에 목표 전송 (피드백 콜백 등록)
        self.get_logger().info(f'목표 전송: distance={distance}')
        future = self._action_client.send_goal_async(
            goal,
            feedback_callback=self._on_feedback     # 피드백 수신 시 호출할 콜백
        )

        # 목표 수락 여부 확인
        rclpy.spin_until_future_complete(self, future)
        goal_handle: ClientGoalHandle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('목표 거절됨.')
            return

        self.get_logger().info('목표 수락됨. 결과 대기 중...')
        
        # 목표 취소 요청 -----------------------------------------------
        # 취소 응답 콜백
        def _on_cancel_response(future):
            cancel_response = future.result()
            if len(cancel_response.goals_canceling) > 0:
                self.get_logger().info('취소 수락됨.')
            else:
                self.get_logger().warn('취소 거절됨.')
        
        # - 별도 스레드에서 3초 후 취소 요청
        def cancel_after_delay():
            time.sleep(2.0)
            cancel_future = goal_handle.cancel_goal_async()         # 취소 요청 전송
            cancel_future.add_done_callback(_on_cancel_response)    # 취소 응답 콜백 등록

        # 취소 요청을 테스트할 때에는 주석 해제
        # threading.Thread(target=cancel_after_delay).start()
        # ------------------------------------------------------------

        # 최종 결과 수신 대기
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        # 결과 처리
        result: Move.Result = result_future.result().result
        self.get_logger().info(
            f'결과 수신: success={result.success}, message={result.message}'
        )


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = MoveClientNode()         # Move 액션 클라이언트 노드 생성

    # 액션 서버가 준비될 때까지 대기
    node._wait_for_server()

    # --- 테스트 시작 ---

    # 5.0m 이동 목표 전송
    node.send_goal(5.0)

    # --- 테스트 완료 ---

    node.destroy_node()         # 노드 자원 해제
    if rclpy.ok():              # ROS 2 런타임이 현재 정상 동작 중인지 확인
        rclpy.shutdown()        # ROS 2 종료
