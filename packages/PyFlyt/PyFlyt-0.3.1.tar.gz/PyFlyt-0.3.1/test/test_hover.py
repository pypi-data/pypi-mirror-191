from pprint import pprint

import gymnasium
import numpy as np

import PyFlyt.gym_envs

env = gymnasium.make("PyFlyt/SimpleHoverEnv-v0", render_mode="human")

for i in range(3):
    obs, info = env.reset()

    term, trunc = False, False
    while not term and not trunc:
        action = np.zeros((4,))

        obs, rew, term, trunc, info = env.step(action)
