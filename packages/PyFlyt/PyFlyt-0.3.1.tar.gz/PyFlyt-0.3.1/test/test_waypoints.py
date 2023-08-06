import glob
import os
from pprint import pprint

import gymnasium
import matplotlib.pyplot as plt
import numpy as np

import PyFlyt.gym_envs

env = gymnasium.make(
    "PyFlyt/SimpleWaypointEnv-v0",
    render_mode="human",
    # render_mode=None,
    use_yaw_targets=False,
    num_targets=10,
)

files = glob.glob("./plots/*")
for f in files:
    os.remove(f)

# this script only works with set mode 6 in the env
fail = 0
success = 0
for trial in range(100):
    time = 0
    obs, info = env.reset()
    term, trunc = False, False
    action = np.array([0, 0, 0, 0])
    gain = 0.5

    # logs
    x_log = []
    y_log = []
    z_log = []
    t_log = []

    while not term and not trunc:
        time += 1

        target = obs["target_deltas"].nodes[0]

        # smooth transition
        action = np.array([target[0], target[1], 0.0, target[2]]) * gain + action * (
            1 - gain
        )

        # step env
        obs, rew, term, trunc, _ = env.step(action)

        x_log.append(target[0])
        y_log.append(target[1])
        z_log.append(target[2])
        t_log.append(time)

    if term:
        fail += 1
        plt.plot(t_log, x_log, "r", t_log, y_log, "g", t_log, z_log, "b")
        plt.savefig(f"./plots/{trial}.png")
        plt.close()
    if trunc:
        success += 1
    print(f"{fail=}, {success=}")
