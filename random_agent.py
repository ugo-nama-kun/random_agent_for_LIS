# -*- coding: utf-8 -*-

import os
import numpy as np


class RandomAgent(object):
    actions = [0, 1, 2]

    def agent_init(self, **options):
        self.time = 0
        print("Agent Initialized!")

    def agent_start(self, observation):
        
        # Generate a Random Action
        action = np.random.randint(len(self.actions))
        return_action = action

        return return_action

    def agent_step(self, reward, observation):
        # Generate a Random Action
        action = np.random.randint(len(self.actions))
        return_action = action


        return action
