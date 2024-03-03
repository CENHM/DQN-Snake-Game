from collections import deque
from collections import namedtuple

from network import DQN
from utils import ACTION, BROAD_WIDTH, BROAD_HEIGHT
from windowsAPI import actions


class Agent:
    def __init__(self):
        self._SNAKE_START_LEN = 4

        self.action = None
        self.snake = deque()
        self.named_tuple = namedtuple('named_tuple', ['x', 'y'])
        self.brain = DQN()

    # def legal_action(self):
    #     t_x, t_y = self.snake[0].x + ACTION[self.action].x, self.snake[0].y + ACTION[self.action].y
    #     # Boundary
    #     if t_x < 0 or t_y < 0 or t_x >= BROAD_WIDTH or t_y >= BROAD_HEIGHT:
    #         return False
    #     # Hit
    #     # for part in self.snake:
    #     #     if t_x == part.x and t_y == part.y:
    #     #         return False
    #     return True

    def init_snake(self):
        self.snake = deque()
        for part_idx in range(self._SNAKE_START_LEN, 0, -1):
            self.snake.append(self.named_tuple(part_idx, 1))

    def new_snake(self):
        self.snake.pop()
        self.snake.appendleft(self.named_tuple(self.snake[0].x + ACTION[self.action][0],
                                               self.snake[0].y + ACTION[self.action][1]))

    def take_action(self, action):
        actions[action]()
        self.action = action
        self.new_snake()

