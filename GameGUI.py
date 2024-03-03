import os
import random
from collections import deque

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from utils import ACTION, BROAD_WIDTH, BROAD_HEIGHT


class SnakeGameGUI:
    def __init__(self, include_timer=True):
        self._SQUARE_SIZE = 40

        self._WINDOW_WIDTH = BROAD_WIDTH * self._SQUARE_SIZE
        self._WINDOW_HEIGHT = BROAD_HEIGHT * self._SQUARE_SIZE

        self.SNAKE_BODY_COLOR = (255, 255, 255)
        self.SNAKE_HEAD_COLOR = (0, 200, 100)

        self.board_height = 600
        self.text_height = 50
        self.text_x_gap = 30

        self.square_len = 40

        self.snake = None
        self.apple = None

        self.background_color = (50, 50, 50)
        self.board_colors = [(18, 18, 18), (12, 12, 12)]



        self.snake_body_color = (255, 255, 255)
        self.snake_head_color = (0, 200, 100)
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

    def render(self, snake, apple):
        if self.window is None:
            self.window = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT))

        self.draw_background()
        self.draw_snake(snake)
        self.draw_apple(apple)
        # self.draw_scores(self.best_score, self.curr_score)
        pygame.display.update()

    def draw_background(self):
        for row in range(BROAD_HEIGHT):
            for column in range(BROAD_WIDTH):
                pygame.draw.rect(self.window, self.board_colors[(row + column) % 2],
                                 [column * self.square_len, row * self.square_len, self.square_len, self.square_len])

    # def draw_scores(self, best_score, curr_score):
    #     assert self.window is not None, 'self.draw_scores (SnakeGUI): window must not be None'
    #
    #     best_score_text = self.font.render(f'Best Score: {best_score}', False, self.scores_color)
    #     curr_score_text = self.font.render(f'Current Score: {curr_score}', False, self.scores_color)
    #
    #     text_size = curr_score_text.get_rect()
    #     text_y_gap = int(self.text_height / 2 - text_size.height / 2)
    #
    #     pygame.draw.rect(self.window, self.background_color,
    #                      [0, self.board_height, self._window_w, self.text_height])
    #     self.window.blit(best_score_text, (self.text_x_gap, self.board_height + text_y_gap))
    #     self.window.blit(curr_score_text,
    #                      (self._window_w - self.text_x_gap - text_size.width, self.board_height + text_y_gap))

    def draw_snake(self, snake):
        color = self.SNAKE_HEAD_COLOR
        for point in snake:
            x, y = point[0] * self.square_len, point[1] * self.square_len
            pygame.draw.rect(self.window, color, [int(x), int(y), self.square_len, self.square_len])
            pygame.draw.rect(self.window, self.snake_border_color,
                             [int(x), int(y), self.square_len, self.square_len], width=1)
            color = self.SNAKE_BODY_COLOR

    def draw_apple(self, apple):
        pygame.draw.rect(self.window, self.apple_color,
                         [apple.x * self.square_len, apple.y * self.square_len, self.square_len,
                          self.square_len])

    def reset(self):
        self.timer = None

    def close(self):
        pygame.display.quit()
        pygame.quit()
        self.window = None
        self.timer = None
