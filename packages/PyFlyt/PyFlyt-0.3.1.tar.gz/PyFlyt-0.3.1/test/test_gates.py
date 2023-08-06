import gymnasium
import numpy as np

import PyFlyt.gym_envs

env = gymnasium.make("PyFlyt/AdvancedGatesEnv-v0", render_mode="human", num_targets=10)

for i in range(3):
    obs, info = env.reset()

    term, trunc = False, False
    while True:
        if not term and not trunc:
            target = obs["target_deltas"].nodes[0]
            action = np.array([target[0], target[1], 0.0, target[2] - 0.1])

            obs, rew, term, trunc, info = env.step(action)
        else:
            term, trunc = False, False
            obs, info = env.reset()
