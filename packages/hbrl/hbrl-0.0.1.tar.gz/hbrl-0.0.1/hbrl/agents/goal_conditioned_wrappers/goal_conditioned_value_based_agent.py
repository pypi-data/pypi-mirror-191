# Goal conditioned agent
from typing import Union

import numpy as np
from gym.spaces import Box, Discrete

from hbrl.agents.goal_conditioned_wrappers.goal_conditioned_agent import GoalConditionedAgent
from hbrl.agents.value_based_agent import ValueBasedAgent


class GoalConditionedValueBasedAgent(GoalConditionedAgent, ValueBasedAgent):
    """
    A global agent class for goal conditioned agents. The # NEW tag indicate differences between Agent class and this
    one.
    """

    def __init__(self, reinforcement_learning_agent_class, state_space: Union[Box, Discrete],
                 action_space: Union[Box, Discrete], **params):
        GoalConditionedAgent.__init__(self, state_space, action_space, **params)
        self.reinforcement_learning_agent_class = reinforcement_learning_agent_class

        # Compute our agent new state space as a goal-conditioned state space (a concatenation of our state space and
        # our goal space)
        self.reinforcement_learning_agent: ValueBasedAgent = \
            reinforcement_learning_agent_class(self.feature_space, action_space, **params)

    def __getattr__(self, name):
        """Returns an attribute with ``name``, unless ``name`` starts with an underscore."""
        if name.startswith("_"):
            raise AttributeError(f"accessing private attribute '{name}' is prohibited")
        return getattr(self.reinforcement_learning_agent, name)

    def learn(self):
        self.reinforcement_learning_agent.learn()

    @property
    def feature_space(self):
        if isinstance(self.state_space, Box) and isinstance(self.goal_space, Box):
            return Box(low=np.concatenate((self.state_space.low, self.goal_space.low)),
                       high=np.concatenate((self.state_space.high, self.goal_space.high)))
        elif isinstance(self.state_space, Discrete) and isinstance(self.goal_space, Discrete):
            return Discrete(self.state_space.n * self.goal_space.n)
        else:
            raise NotImplementedError("State space ang goal space with different types are not supported.")

    def get_features(self, states, goals):
        if isinstance(self.state_space, Box) and isinstance(self.goal_space, Box):
            return np.concatenate((states, goals), -1)
        elif isinstance(self.state_space, Discrete) and isinstance(self.goal_space, Discrete):
            return states + goals * self.state_space.n  # Use a bijection between N² and N
        else:
            raise NotImplementedError("State space ang goal space with different types are not supported.")

    def get_value(self, state, goal, actions=None):
        return self.reinforcement_learning_agent.get_value(self.get_features(state, goal), actions)

    def start_episode(self, state: np.ndarray, goal: np.ndarray, test_episode=False):
        GoalConditionedAgent.start_episode(self, state, goal, test_episode)
        self.reinforcement_learning_agent.start_episode(self.get_features(state, self.current_goal), test_episode)

    def action(self, state, explore=True):
        return self.reinforcement_learning_agent.action(self.get_features(state, self.current_goal), explore)

    def process_interaction(self, action, reward, new_state, done, learn=True):
        super().process_interaction(action, reward, new_state, done, learn=learn)
        new_state = self.get_features(new_state, self.current_goal)
        self.reinforcement_learning_agent.process_interaction(action, reward, new_state, done, learn)

    def save_interaction(self, state, action, reward, new_state, done, goal=None):
        assert not self.under_test
        goal = self.current_goal if goal is None else goal
        state = self.get_features(state, goal)
        new_state = self.get_features(new_state, goal)
        self.reinforcement_learning_agent.save_interaction(state, action, reward, new_state, done)

    def get_estimated_distances(self, states, goals):
        """
        Return the estimated distance between given goals and states.
        """
        features = self.get_features(states, goals)
        estimated_distance = self.reinforcement_learning_agent.get_value(features)
        if len(estimated_distance.shape) == 0:
            estimated_distance = estimated_distance.reshape((1,))
        estimated_distance = - estimated_distance.clip(float("-inf"), 0)
        return estimated_distance

    def reset(self):
        self.__init__(self.reinforcement_learning_agent_class, self.state_space, self.action_space, **self.init_params)

if __name__ == "__main__":
    from hbrl.agents.discrete.dqn import DQN
    from hbrl.environments.grid_world.goal_conditioned_discrete_grid_world import GoalConditionedDiscreteGridWorld

    environment = GoalConditionedDiscreteGridWorld()
    dqn_agent = DQN(action_space=environment.action_space, state_space=environment.state_space)

    new_agent = GoalConditionedValueBasedAgent(DQN, action_space=environment.action_space, state_space=environment.state_space)
    same_buffers = id(new_agent.replay_buffer) == id(new_agent.reinforcement_learning_agent.replay_buffer)

    state, goal = environment.reset()
    print("state: ", state, "; goal: ", goal, "; features: ", new_agent.get_features(state, goal))

    new_agent.start_episode(state, goal)
    print(new_agent.action(state))

    a = 1
