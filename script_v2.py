import unittest


class Solution:
    @staticmethod
    def robot_sim(commands: list[int], obstacles: list[list[int]]) -> int:
        # Direction vectors: North, East, South, West
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        obstacle_set = set(map(tuple, obstacles))

        dir_idx = 0  # Start facing North
        x, y = 0, 0
        max_dist = 0

        for cmd in commands:
            if cmd == -2:
                dir_idx = (dir_idx - 1) % 4   # turn left
            elif cmd == -1:
                dir_idx = (dir_idx + 1) % 4   # turn right
            else:
                dx, dy = directions[dir_idx]
                for _ in range(cmd):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in obstacle_set:
                        break          # blocked, stop moving this command
                    x, y = nx, ny
                    max_dist = max(max_dist, x * x + y * y)

        return max_dist


class TestRobotSim(unittest.TestCase):

    def test_example1_basic_movement(self):
        # Walk 4 north -> turn right -> walk 3 east: reaches (3,4), dist^2 = 25
        sol = Solution()
        self.assertEqual(sol.robotSim([4, -1, 3], []), 25)

    def test_example2_obstacle_blocks_partial(self):
        # Obstacle at (2,4) cuts northward leg short; max reached is (1,8), dist^2 = 65
        sol = Solution()
        self.assertEqual(sol.robotSim([4, -1, 4, -2, 4], [[2, 4]]), 65)

    def test_example3_obstacle_at_origin(self):
        # Obstacle at origin is naturally skipped while robot is there;
        # blocks return to (0,0) after moving away. Max is (0,6), dist^2 = 36.
        sol = Solution()
        self.assertEqual(sol.robotSim([6, -1, -1, 6], [[0, 0]]), 36)

    def test_only_turns_no_movement(self):
        # No forward commands, robot stays at origin the whole time
        sol = Solution()
        self.assertEqual(sol.robotSim([-1, -2, -1], []), 0)

    def test_single_forward_command(self):
        # Walk 3 steps north: reaches (0,3), dist^2 = 9
        sol = Solution()
        self.assertEqual(sol.robotSim([3], []), 9)

    def test_obstacle_at_start_blocks_return(self):
        # Walk 1 north, turn right twice (now facing south), walk 1 south;
        # obstacle at origin blocks return; max is (0,1), dist^2 = 1.
        sol = Solution()
        self.assertEqual(sol.robotSim([1, -1, -1, 1], [[0, 0]]), 1)

    def test_obstacle_immediately_ahead(self):
        # Obstacle at (0,1) blocks the very first step north; robot never moves
        sol = Solution()
        self.assertEqual(sol.robotSim([5], [[0, 1]]), 0)

    def test_full_circle_no_obstacles(self):
        # Alternating 1-step forward and right turns traces a 1x1 square;
        # max squared distance is always 1
        sol = Solution()
        self.assertEqual(sol.robotSim([1, -1, 1, -1, 1, -1, 1, -1], []), 1)


if __name__ == "__main__":
    unittest.main()
