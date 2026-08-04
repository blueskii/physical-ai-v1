import rclpy                                            # ROS 2 Python 클라이언트 라이브러리
from rclpy.node import Node                             # ROS 2 노드 기본 클래스
from rclpy.action import ActionServer                   # 액션 서버 클래스
from rclpy.action import GoalResponse, CancelResponse   # 목표 수락/거절 응답 타입, 취소 수락/거절 응답 타입
from rclpy.action.server import ServerGoalHandle        # 목표 핸들 (피드백 전송, 결과 설정에 사용)
from robot_interfaces.action import Move                # Move 액션 타입 (Goal/Result/Feedback)
import time                                             # 피드백 전송 간격 조절용

# Move 액션 서버 노드
class MoveServerNode(Node):
    def __init__(self):
        # 부모 초기화 메소드 호출: 노드 이름 등록
        super().__init__('move_server_node')

        # Move 액션 서버 생성
        self._action_server = ActionServer(
            self,                                       # 노드
            Move,                                       # 액션 타입
            '/action/move',                             # 액션 이름
            goal_callback=self._handle_goal_accept,     # 목표 수락/거절 콜백            
            cancel_callback=self._handle_cancel_accept, # 취소 수락/거절 콜백
            execute_callback=self._handle_goal,         # 목표 실행 콜백
        )

        self.get_logger().info('Move 액션 서버 시작됨.')

    # 목표 수락/거절 콜백: 목표가 유효한지 검사
    def _handle_goal_accept(self, goal_request: Move.Goal):
        if goal_request.distance <= 0:
            self.get_logger().warn(f'목표 거절: distance={goal_request.distance} (0 이하 불가)')
            return GoalResponse.REJECT  # 목표 거절
        self.get_logger().info(f'목표 수락: distance={goal_request.distance}')
        return GoalResponse.ACCEPT      # 목표 수락
    
    # 취소 수락/거절 콜백
    def _handle_cancel_accept(self, goal_handle):
        return CancelResponse.ACCEPT    # 취소 허용

    # 목표 실행 콜백: Goal → Feedback 반복 → Result 순으로 처리
    def _handle_goal(self, goal_handle: ServerGoalHandle):
        # 목표 수신
        goal: Move.Goal = goal_handle.request
        self.get_logger().info(f'목표 수신: distance={goal.distance}')
        # 피드백 객체 생성
        feedback = Move.Feedback()
        # 목표 거리까지 0.1씩 이동하며 피드백 전송
        current = 0.0
        step = goal.distance / 10.0     # 10단계로 나눠서 이동
        for i in range(10):
            if goal_handle.is_cancel_requested:   # 취소 요청 감지
                # 액션 상태를 CANCELED로 변경
                # - 호출하지 않으면 클라이언트의 goal_handle.get_result_async()가 완료되지 않고 무한 대기
                goal_handle.canceled()
                # 취소 결과 생성 및 반환
                result = Move.Result()
                result.success = False
                result.message = '취소됨'
                return result            
            current += step             # 현재 이동 거리 누적
            current = round(current, 4) # 소수점 4자리로 반올림
            # 피드백 업데이트
            feedback.current_distance = current
            feedback.progress = current / goal.distance     # 0.0 ~ 1.0
            # 피드백 전송
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f'피드백 전송: current={feedback.current_distance:.2f}, '
                f'progress={feedback.progress:.0%}'     # 0.75 -> 75%로 출력
            )
            time.sleep(0.5)     # 0.5초 간격으로 이동 시뮬레이션
            
        # 목표 달성 완료 통보
        # - 성공: goal_handle.succeed()
        # - 실패: goal_handle.abort()
        # - 이중 하나를 호출하지 않으면 클라이언트의 goal_handle.get_result_async()가 완료되지 않고 무한 대기
        # - 결과 데이터는 return 값으로 전달
        goal_handle.succeed()

        # 완료 결과 생성 및 반환
        result = Move.Result()
        result.success = True
        result.message = f'{goal.distance}m 이동 완료'
        self.get_logger().info(f'결과 전송: {result.message}')
        return result


def main(args=None):
    rclpy.init(args=args)           # ROS 2 초기화
    node = MoveServerNode()         # Move 액션 서버 노드 생성
    # MultiThreadedExecutor: _handle_goal 실행 중에도 cancel_callback 처리 가능
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()             # 노드 실행 (종료 신호가 올 때까지 대기)
    except KeyboardInterrupt:
        pass                        # Ctrl+C 로 종료 시 정상 처리
    finally:
        node.destroy_node()         # 노드 자원 해제
        if rclpy.ok():              # ROS 2 런타임이 현재 정상 동작 중인지 확인
            rclpy.shutdown()        # ROS 2 종료
