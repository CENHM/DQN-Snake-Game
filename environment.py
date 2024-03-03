import random
from collections import namedtuple

import torch
import win32gui, win32print, win32api
from PIL import ImageGrab, Image  # 操作图像
import win32con  # 系统操作
import numpy as np
import cv2

from utils import BROAD_WIDTH, BROAD_HEIGHT


class Environment:
    def __init__(self):
        self.frame = None
        self.apple = None

    def init_apple(self, snake):
        named_tuple = namedtuple('named_tuple', ['x', 'y'])
        while True:
            done = True
            self.apple = named_tuple(random.randint(0, BROAD_WIDTH - 1), random.randint(0, BROAD_HEIGHT - 1))
            for part in snake:
                if self.apple.x == part.x and self.apple.y == part.y:
                    done = False
                    break
            if done:
                break

    def get_frame(self):
        window = win32gui.FindWindow(0, 'pygame window')
        hDC = win32gui.GetDC(0)
        real_w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        apparent_w = win32api.GetSystemMetrics(0)
        scale_radio = real_w / apparent_w
        origin_window_react = win32gui.GetWindowRect(window)
        fixed_window_react = [item * scale_radio for item in origin_window_react]
        image = ImageGrab.grab(fixed_window_react)

        image = np.array(image)[39:839, 10:810, :]

        image = cv2.resize(np.array(image), (224, 224)).transpose(2, 0, 1)
        image = torch.tensor(image).to(torch.float32)
        image = torch.unsqueeze(image, 0)
        self.frame = image

    def get_reward(self, snake):
        x, y = snake[0].x, snake[0].y
        # Boundary
        if x < 0 or y < 0 or x >= BROAD_WIDTH or y >= BROAD_HEIGHT:
            # print("Hit boundary. Lose.")
            return -100., True, False
        # Hit
        cnt = True
        for part in snake:
            if cnt:
                cnt = False
                continue
            if x == part.x and y == part.y:
                # print("Hit yourself. Lose.")
                return -100., True, False
        if x == self.apple.x and y == self.apple.y:
            # print("Nice work.")
            return 200., False, True
        # print("Move.")
        return 1., False, False
