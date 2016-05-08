# -*- coding: utf-8 -*-

import os
import numpy as np
from chainer import cuda


class RandomAgent(object):
    actions = [0, 1, 2]

    def agent_init(self, **options):
        self.time = 0

    def agent_start(self, observation):
        image = observation["image"]
        depth = observation["depth"]
        temperature = observation["temperature"]

        print("temperature :: " + str(temperature))
        # Generate a Random Action
        action = np.random.randint(len(self.actions))
        return_action = action

        return return_action

    def agent_step(self, reward, observation):
        image = observation["image"]
        depth = observation["depth"]
        temperature = observation["temperature"]

        print("temperature :: " + str(temperature))
        # Generate a Random Action
        action = np.random.randint(len(self.actions))
        return_action = action


        return action
