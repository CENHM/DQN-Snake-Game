import random
import time

from GameGUI import SnakeGameGUI
from environment import get_frame
from utils import ACTION


def main():
    env = SnakeGameGUI()
    while True:

        action = random.randint(0, len(ACTION) - 1)
        env.render(action)
        time.sleep(1)
        get_frame()
        time.sleep(1)


if __name__ == "__main__":
    main()
