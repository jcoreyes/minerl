from gym.envs.registration import register
from collections import OrderedDict
from minerl.env import spaces
from minerl.env.core import MineRLEnv
import os

import numpy as np


missions_dir = os.path.join(os.path.dirname(__file__), 'missions')

register(
    id='MineRLWoolGatheringTrain-v0',
    entry_point='minerl.env:MineRLEnv',
    kwargs={
        'xml': os.path.join(missions_dir, 'wool_gather_train.xml'),
        'observation_space': spaces.Dict({
            'pov': spaces.Box(low=0, high=255, shape=(64, 64, 3), dtype=np.uint8),
        }),
        'action_space': spaces.Dict(spaces={
            "forward": spaces.Discrete(2),
            "back": spaces.Discrete(2),
            "left": spaces.Discrete(2),
            "right": spaces.Discrete(2),
            "jump": spaces.Discrete(2),
            "sneak": spaces.Discrete(2),
            "sprint": spaces.Discrete(2),
            "attack": spaces.Discrete(2),
            "camera": spaces.Box(low=-180, high=180, shape=(2,), dtype=np.float32),
        }),
    },
    max_episode_steps=8000,
    reward_threshold=1000.0,
)

register(
    id='MineRLWoolGatheringTest-v0',
    entry_point='minerl.env:MineRLEnv',
    kwargs={
        'xml': os.path.join(missions_dir, 'wool_gather_test.xml'),
        'observation_space': spaces.Dict({
            'pov': spaces.Box(low=0, high=255, shape=(64, 64, 3), dtype=np.uint8),
        }),
        'action_space': spaces.Dict(spaces={
            "forward": spaces.Discrete(2),
            "back": spaces.Discrete(2),
            "left": spaces.Discrete(2),
            "right": spaces.Discrete(2),
            "jump": spaces.Discrete(2),
            "sneak": spaces.Discrete(2),
            "sprint": spaces.Discrete(2),
            "attack": spaces.Discrete(2),
            "camera": spaces.Box(low=-180, high=180, shape=(2,), dtype=np.float32),
        }),
    },
    max_episode_steps=8000,
    reward_threshold=1000.0,
)