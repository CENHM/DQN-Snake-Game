import os
import random
from collections import deque

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from utils import ACTION


class SnakeGameGUI:
    def __init__(self, include_timer=True):

        self.w = 16
        self.h = 16

        self._window_w = 640
        self._window_h = 640

        self.board_height = 600
        self.text_height = 50
        self.text_x_gap = 30

        self.square_len = 40

        self.snake = None
        self.apple = None

        self.background_color = (50, 50, 50)
        self.board_colors = [(18, 18, 18), (12, 12, 12)]


        self.snake_body_color = (255, 255, 255)
        self.snake_head_color = (0, 252, 0)
        self.snake_border_color = (0, 0, 0)

        self.apple_color = (255, 0, 0)
        self.scores_color = (255, 255, 255)

        self.right_key = pygame.K_RIGHT
        self.left_key = pygame.K_LEFT
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN
        self.switch_mode_key = pygame.K_SPACE

        self.timer = None
        self.include_timer = include_timer

        self.update_delay_sec = .120
        self.max_user_actions_per_update = 2

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Ariel', 30)

        self.window = None

        self.best_score = 0
        self.curr_score = 0

    def init_snake(self):
        _SNAKE_START_LEN = 4
        self.snake = deque()
        for part_idx in range(_SNAKE_START_LEN, 0, -1):
            self.snake.append((part_idx, 1))

    def render(self, action):
        if self.window is None:
            self.window = pygame.display.set_mode((self._window_w, self._window_h))
        if self.snake is None:
            self.init_snake()


        self.draw_background()
        self.draw_snake(action)
        # self.draw_apple(self.apple)
        # self.draw_scores(self.best_score, self.curr_score)
        pygame.display.update()

    def draw_background(self):
        assert self.window is not None, 'self.draw_background (SnakeGUI): window must not be None'

        for row in range(self.h):
            for column in range(self.w):
                pygame.draw.rect(self.window, self.board_colors[(row + column) % 2],
                                 [column * self.square_len, row * self.square_len, self.square_len, self.square_len])

    def draw_scores(self, best_score, curr_score):
        assert self.window is not None, 'self.draw_scores (SnakeGUI): window must not be None'

        best_score_text = self.font.render(f'Best Score: {best_score}', False, self.scores_color)
        curr_score_text = self.font.render(f'Current Score: {curr_score}', False, self.scores_color)

        text_size = curr_score_text.get_rect()
        text_y_gap = int(self.text_height / 2 - text_size.height / 2)

        pygame.draw.rect(self.window, self.background_color,
                         [0, self.board_height, self._window_w, self.text_height])
        self.window.blit(best_score_text, (self.text_x_gap, self.board_height + text_y_gap))
        self.window.blit(curr_score_text,
                         (self._window_w - self.text_x_gap - text_size.width, self.board_height + text_y_gap))

    def draw_snake(self, action):
        assert self.snake is not None, 'self.draw_snake (SnakeGUI): snake must not be None'
        assert self.window is not None, 'self.draw_snake (SnakeGUI): window must not be None'

        color = self.snake_head_color

        if self.snake[0][0] + ACTION[action][0] < 0 or self.snake[0][0] + ACTION[action][0] >= self.w or \
           self.snake[0][1] + ACTION[action][1] < 0 or self.snake[0][1] + ACTION[action][1] >= self.h:
            pass
        else:
            self.snake.pop()
            self.snake.appendleft((self.snake[0][0] + ACTION[action][0], self.snake[0][1] + ACTION[action][1]))

        for point in self.snake:
            x, y = point[0] * self.square_len, point[1] * self.square_len
            pygame.draw.rect(self.window, color, [int(x), int(y), self.square_len, self.square_len])
            pygame.draw.rect(self.window, self.snake_border_color,
                             [int(x), int(y), self.square_len, self.square_len], width=1)

            color = self.snake_body_color

    def draw_apple(self, apple):
        assert apple is not None, 'self.draw_apple (SnakeGUI): apple must not be None'
        assert self.window is not None, 'self.draw_apple (SnakeGUI): window must not be None'

        pygame.draw.rect(self.window, self.apple_color,
                         [apple.column * self.square_len, apple.row * self.square_len, self.square_len,
                          self.square_len])

    def reset(self):
        self.timer = None

    def close(self):
        pygame.display.quit()
        pygame.quit()
        self.window = None
        self.timer = None
