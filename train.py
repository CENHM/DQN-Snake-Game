import time

from Agent import Agent
from GameGUI import SnakeGameGUI
from environment import Environment
from utils import EPISODE, EPSILON


def main():
    playground = SnakeGameGUI()
    agent = Agent()
    environment = Environment()

    for i in range(EPISODE):
        print(f"Episode {i}")

        end = False

        agent.init_snake()
        environment.init_apple(agent.snake)
        playground.render(agent.snake, environment.apple)

        environment.get_frame()
        while not end:
            s_c = environment.frame
            a_c = agent.brain.choose_action(s_c)

            agent.take_action(a_c)
            playground.render(agent.snake, environment.apple)

            environment.get_frame()
            s_n = environment.frame

            r_c, end = environment.get_reward(agent.snake)

            agent.brain.store_transition(s_c, a_c, r_c, s_n)

            agent.brain.check_learn()
            time.sleep(0.1)
        # print(f"episode_r_a: {episode_r_a}, episode_r_d: {episode_r_a}")


if __name__ == "__main__":
    main()