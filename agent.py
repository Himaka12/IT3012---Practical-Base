# agent.py
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