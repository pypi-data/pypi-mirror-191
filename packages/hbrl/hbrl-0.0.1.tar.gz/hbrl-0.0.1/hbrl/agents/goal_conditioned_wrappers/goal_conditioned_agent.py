# Goal conditioned agent
from typing import Union

import numpy as np
from gym.spaces import Box, Discrete
from hbrl.agents.agent import Agent


class GoalConditionedAgent(Agent):
    """
    A global agent class for goal conditioned agents. The # NEW tag indicate differences between Agent class and this
    one.
    """

    name = "Default goal conditioned agent"

    def __init__(self, state_space: Union[Box, Discrete], action_space: Union[Box, Discrete], **params):
        Agent.__init__(self, state_space, action_space, **params)
        self.current_goal = None

        # Compute out goal space
        self.goal_space = params.get("goal_space", self.state_space)
        assert isinstance(self.goal_space, Box) or isinstance(self.goal_space, Discrete)
        self.goal_size = self.goal_space.shape[0]
        self.goal_shape = self.goal_space.shape
        assert len(self.goal_shape) == 1, "Multi dimensional spaces are not supported."

        # Compute state_to_goal_filter, (state[self.state_to_goal_filter] = <goal associated to state>) aka a projection
        default_filter = np.array([1] * self.goal_size + [0] * (self.state_size - self.goal_size)).astype(bool)
        self.state_to_goal_filter = params.get("state_to_goal_filter", default_filter)
        assert np.argwhere(self.state_to_goal_filter).shape[0] == self.goal_size

    def start_episode(self, state: np.ndarray, goal: np.ndarray, test_episode=False):
        super().start_episode(state, test_episode)
        self.current_goal = goal

    def reset(self):
        self.__init__(self.state_space, self.action_space, **self.init_params)
