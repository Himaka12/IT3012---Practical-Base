# agent.py
from collections import deque
import heapq
import math

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:

    def sense_and_act(self, percept: dict) -> str:
        direction = percept['facing_direction']

        if percept['food_here']:
            return direction

        if percept['wall_ahead']:
            turns = {
                'Up': 'Left',
                'Left': 'Down',
                'Down': 'Right',
                'Right': 'Up'
            }
            return turns[direction]

        return direction

class ModelBasedAgent:

    def __init__(self):
        self.relative_pos = (0, 0)
        self.visited_cells = {(0, 0)}
        self.last_action = None
        self.last_percept = None

    def sense_and_act(self, percept: dict) -> str:
        # Update internal position from the last action
        if self.last_action is not None:
            x, y = self.relative_pos

            if self.last_action == 'Up':
                y += 1
            elif self.last_action == 'Down':
                y -= 1
            elif self.last_action == 'Left':
                x -= 1
            elif self.last_action == 'Right':
                x += 1

            self.relative_pos = (x, y)

        # Record current state
        self.visited_cells.add(self.relative_pos)
        self.last_percept = percept.copy()

        direction = percept['facing_direction']

        turns_left = {
            'Up': 'Left',
            'Left': 'Down',
            'Down': 'Right',
            'Right': 'Up'
        }

        turns_right = {
            'Up': 'Right',
            'Right': 'Down',
            'Down': 'Left',
            'Left': 'Up'
        }

        left_direction = turns_left[direction]
        right_direction = turns_right[direction]

        x, y = self.relative_pos

        moves = {
            'Up': (x, y + 1),
            'Down': (x, y - 1),
            'Left': (x - 1, y),
            'Right': (x + 1, y)
        }

        forward_cell = moves[direction]
        left_cell = moves[left_direction]
        right_cell = moves[right_direction]

        # Use memory to avoid repeating visited paths
        if percept['wall_ahead']:
            if left_cell not in self.visited_cells:
                action = left_direction
            else:
                action = right_direction
        elif forward_cell in self.visited_cells:
            if left_cell not in self.visited_cells:
                action = left_direction
            elif right_cell not in self.visited_cells:
                action = right_direction
            else:
                action = right_direction
        else:
            action = direction

        self.last_action = action
        return action

class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'
        self.current_pos = (0, 0)
        self.last_action = None

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2
            + (pos[1] - goal[1]) ** 2
        )

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        frontier = deque([(start_pos, [])])
        reached = {start_pos}

        while frontier:
            current_pos, path = frontier.popleft()

            if current_pos == goal_pos:
                return path

            x, y = current_pos

            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos

                if (
                    0 <= nx < grid_size[0]
                    and 0 <= ny < grid_size[1]
                    and next_pos not in walls
                    and next_pos not in reached
                ):
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))

        return []

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        frontier = [(start_pos, [])]
        reached = {start_pos}

        while frontier:
            current_pos, path = frontier.pop()

            if current_pos == goal_pos:
                return path

            x, y = current_pos

            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos

                if (
                    0 <= nx < grid_size[0]
                    and 0 <= ny < grid_size[1]
                    and next_pos not in walls
                    and next_pos not in reached
                ):
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))

        return []

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        frontier = [(0, start_pos, [])]
        reached = set()

        while frontier:
            cost, current_pos, path = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path

            if current_pos in reached:
                continue

            reached.add(current_pos)

            x, y = current_pos

            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos

                if (
                    0 <= nx < grid_size[0]
                    and 0 <= ny < grid_size[1]
                    and next_pos not in walls
                    and next_pos not in reached
                ):
                    new_cost = cost + 1
                    heapq.heappush(
                        frontier,
                        (new_cost, next_pos, path + [action])
                    )

        return []

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        frontier = []
        reached_states = set()

        if heuristic_type == 'euclidean':
            h_cost = self.euclidean_distance(start_pos, goal_pos)
        else:
            h_cost = self.manhattan_distance(start_pos, goal_pos)

        heapq.heappush(
            frontier,
            (h_cost, 0, start_pos, [])
        )

        while frontier:
            f_cost, g_cost, current_pos, path = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            x, y = current_pos

            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos

                if (
                    0 <= nx < grid_size[0]
                    and 0 <= ny < grid_size[1]
                    and next_pos not in walls
                    and next_pos not in reached_states
                ):
                    new_g_cost = g_cost + 1

                    if heuristic_type == 'euclidean':
                        new_h_cost = self.euclidean_distance(
                            next_pos,
                            goal_pos
                        )
                    else:
                        new_h_cost = self.manhattan_distance(
                            next_pos,
                            goal_pos
                        )

                    new_f_cost = new_g_cost + new_h_cost

                    heapq.heappush(
                        frontier,
                        (
                            new_f_cost,
                            new_g_cost,
                            next_pos,
                            path + [action]
                        )
                    )

        return []

    def sense_and_act(self, percept: dict) -> str:
        # Update current position from the previous action
        if self.last_action is not None:
            x, y = self.current_pos

            if self.last_action == 'Up':
                y += 1
            elif self.last_action == 'Down':
                y -= 1
            elif self.last_action == 'Left':
                x -= 1
            elif self.last_action == 'Right':
                x += 1

            self.current_pos = (x, y)
            self.last_action = None

        # Create a new plan when the current plan is empty
        if not self.plan:
            food_positions = percept['all_food']

            if not food_positions:
                return 'Up'

            goal_pos = min(
                food_positions,
                key=lambda food: abs(food[0] - self.current_pos[0])
                + abs(food[1] - self.current_pos[1])
            )

            walls = set(percept['walls'])
            grid_size = percept['grid_size']

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(
                    self.current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(
                    self.current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(
                    self.current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )

        if self.plan:
            action = self.plan.pop(0)
            self.last_action = action
            return action

        return 'Up'