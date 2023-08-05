import os.path
from copy import deepcopy

import numpy as np
import torch.cuda
from statistics import mean
from hbrl.agents import DistributionalDQN

from hbrl.agents import HER
from hbrl.agents.continuous.sac import SAC
from hbrl.agents.continuous.ddpg import DDPG
from hbrl.agents.global_planning.reachability_graph_learning.sgm import SGM
from hbrl.agents.global_planning.sub_goal_generation_learning.hrl import HRL
from hbrl.environments import plot_graph_on_environment, GoalConditionedDiscreteGridWorld
from hbrl.agents.global_planning.reachability_graph_learning.sorb import SORB
from hbrl.environments.point_env.goal_conditioned_point_env import GoalConditionedPointEnv
import matplotlib.pyplot as plt
from hbrl.utils import get_red_green_color, save_image, generate_video
from hbrl.agents.goal_conditioned_wrappers.tilo import TILO
from hbrl.environments import MapsIndex
from hbrl.agents.goal_conditioned_wrappers.goal_conditioned_value_based_agent import GoalConditionedValueBasedAgent


def show_q_value(env: GoalConditionedPointEnv, c51_agent, image_id):
    output_dir = os.path.dirname(__file__) + "/directory/"
    oracle = env.get_oracle()
    initial_state, _ = deepcopy(env).reset()

    image = env.render(ignore_rewards=True)
    q_values = []
    for s in oracle:
        q_values.append(c51_agent.get_q_value(initial_state, s))

    mini, maxi = min(q_values), max(q_values)
    for q_val, s in zip(q_values, oracle):
        value = (q_val - mini) / (maxi - mini)
        env.set_tile_color(image, *env.get_coordinates(s), get_red_green_color(value, hexadecimal=False))

    save_image(image, directory=output_dir, file_name="image_" + str(image_id))


def get_score(agent, environment, nb_episodes, nb_interactions_per_episode, trial=None):
    episodes_before_video = 10
    results_running_average = []
    episodes_results = []
    sub_goals_colors = [[187, 181, 189], [170, 109, 163], [177, 24, 200]]
    videos_output_dir = os.path.dirname(__file__) + "/outputs/"

    if isinstance(agent, HRL):
        pre_train_results = []
        pre_train_running_average_results = []
        training_agent = agent.get_layer(0) if isinstance(agent, HRL) else agent.get_layer(0)
        for episode_id in range(150):
            pre_train_results.append(0)
            state, goal = environment.reset()
            training_agent.start_episode(state, goal)

            for interaction_id in range(100):
                action = training_agent.action(state)
                state, reward, done = environment.step(action)
                training_agent.process_interaction(action, reward, state, done)
                if done:
                    pre_train_results[-1] = 1
                    break
            training_agent.stop_episode()

            if len(pre_train_results) > 20:
                average = mean(pre_train_results[-20:])
                pre_train_running_average_results.append(average)
            else:
                average = mean(pre_train_results)
            print("episode ", episode_id, " average accuracy ", average)
        print("pre_train result: ")
        print(pre_train_running_average_results)

    for episode_id in range(nb_episodes):
        graph_navigation = isinstance(agent, SORB) and agent.graph_up_to_date
        episodes_results.append(0)
        state, goal = environment.reset()
        agent.start_episode(state, goal)

        if episodes_before_video is not None and episode_id % episodes_before_video == 0:
            image = environment.render()
            values = []
            for state_ in environment.get_oracle():
                if isinstance(agent, HRL):
                    value = agent.get_layer(0).get_value(np.array([0, 0]).astype(float), state_)
                elif isinstance(agent, GoalConditionedValueBasedAgent):
                    value = agent.get_value(np.array([0, 0]).astype(float), state_)
                else:
                    break
                values.append(value.item())

            if values:
                value_max = max(values)
                value_min = min(values)

                for state_, value in zip(environment.get_oracle(), values):
                    value_color = get_red_green_color((value - value_min) / (value_max - value_min), hexadecimal=False)
                    environment.set_tile_color(image, *environment.get_coordinates(state_), value_color)
                save_image(image, os.path.dirname(__file__) + "/outputs/value_images/",
                           "episode_" + str(episode_id) + ".png")
            """
            if isinstance(agent, HRL) or isinstance(agent, HRL_TEST2) and episode_id != 0:
                batch = agent.high_level_agent.sample_training_batch(500)

                sample_id = 0
                for s, action, reward, s_, done in zip(*batch):
                    s = s.detach().cpu().numpy()
                    action = action.detach().cpu().numpy()
                    reward = reward.detach().cpu().numpy()
                    s_ = s_.detach().cpu().numpy()
                    done = done.detach().cpu().numpy()
                    assert (s[2:] == s_[2:]).all()
                    sample_id += 1
                    image = environment.get_environment_background(ignore_agent=True, ignore_rewards=True)
                    image = environment.place_point(image, s[:2], [150, 150, 150])
                    if not done:
                        image = environment.place_point(image, s_[:2], [80, 80, 80])
                    if reward == -15:
                        dir_name = "penalized"
                        action_color = [255, 0, 0]
                    elif reward == -1:
                        dir_name = "medium"
                        action_color = [255, 153, 51]
                    else:
                        dir_name = "rewarded"
                        action_color = [0, 255, 0]
                    image = environment.place_point(image, action, action_color)
                    image = environment.place_point(image, s[2:], [0, 0, 0])
                    save_image(image, os.path.dirname(__file__) + "/outputs/high_level_samples/" + dir_name + "/episode_"
                               + str(episode_id) + "/", "sample_" + str(sample_id) + ".mp4")
            """

            # Plot mid level value function
            if isinstance(agent, HRL):

                image = environment.render()
                values = []
                for state_ in environment.get_oracle():
                    value = agent.get_layer(1).high_level_agent.get_value(state, goal, actions=state_)
                    values.append(value.item())

                if values:
                    value_max = max(values)
                    value_min = min(values)
                    for state_, value in zip(environment.get_oracle(), values):
                        value_color = get_red_green_color((value - value_min) / (value_max - value_min), hexadecimal=False)
                        environment.set_tile_color(image, *environment.get_coordinates(state_), value_color)
                    environment.place_point(image, state, [255, 255, 255])
                    environment.place_point(image, goal, [0, 0, 0])
                    save_image(image, os.path.dirname(__file__) + "/outputs/mi_level_value_images/",
                               "episode_" + str(episode_id) + ".png")

                if agent.layer_id == 2:

                    image = environment.render()
                    values = []
                    for state_ in environment.get_oracle():
                        value = agent.get_layer(2).high_level_agent.get_value(state, goal, actions=state_)
                        values.append(value.item())

                    if values:
                        value_max = max(values)
                        value_min = min(values)
                        for state_, value in zip(environment.get_oracle(), values):
                            value_color = get_red_green_color((value - value_min) / (value_max - value_min),
                                                              hexadecimal=False)
                            environment.set_tile_color(image, *environment.get_coordinates(state_), value_color)
                        environment.place_point(image, state, [255, 255, 255])
                        environment.place_point(image, goal, [0, 0, 0])
                        save_image(image, os.path.dirname(__file__) + "/outputs/mi_level_value_images/",
                                   "episode_" + str(episode_id) + ".png")

        if episodes_before_video is not None and episode_id % episodes_before_video == 0:
            if isinstance(agent, HRL):
                images = {
                    "global": [],
                    "low_level_view":[]
                }

                image = environment.render()
                sub_goals = agent.sub_goals
                for sub_goal_id, sub_goal in enumerate(sub_goals):
                    environment.place_point(image, sub_goal, sub_goals_colors[sub_goal_id])
                images["global"].append(image)

                image = environment.render()
                image = environment.place_point(image, agent.get_layer(0).current_goal, sub_goals_colors[0])
                images["low_level_view"].append(image)

        interaction_id = 0
        while True:
            action = agent.action(state)
            state, reward, done = environment.step(action)
            learn = False if graph_navigation else True
            agent.process_interaction(action, reward, state, done, learn=learn)
            if episodes_before_video is not None and episode_id % episodes_before_video == 0:
                if isinstance(agent, HRL):
                    image = environment.render()
                    sub_goals = agent.sub_goals
                    for sub_goal_id, sub_goal in enumerate(sub_goals):
                        environment.place_point(image, sub_goal, sub_goals_colors[sub_goal_id])
                    images["global"].append(image)
                    save_image(image, videos_output_dir + "/global_videos/episode_" + str(episode_id)
                               + "/", "interaction_" + str(interaction_id))

                    image = environment.render()
                    image = environment.place_point(image, agent.get_layer(0).current_goal, sub_goals_colors[0])
                    images["low_level_view"].append(image)

            if done:
                episodes_results[-1] = 1
                break

            if isinstance(agent, SORB) or isinstance(agent, HRL):
                if agent.done:
                    break
            elif interaction_id > nb_interactions_per_episode:
                break

            interaction_id += 1

        agent.stop_episode()
        assert len(episodes_results) == episode_id + 1
        if episodes_before_video is not None and episode_id % episodes_before_video == 0:
            if isinstance(agent, HRL):
                generate_video(images["global"], videos_output_dir + "/global_videos/", "episode_" + str(episode_id))
                generate_video(images["low_level_view"], videos_output_dir + "/low_level_view_videos/",
                               "episode_" + str(episode_id))

        if len(episodes_results) > 20:
            running_average = mean(episodes_results[-20:])
            results_running_average.append(running_average)
        else:
            running_average = mean(episodes_results)
        if isinstance(agent, SORB) and episode_id == nb_episodes - 30:
            agent.build_graph(environment)
            # Plot agent graph
            image = plot_graph_on_environment(agent.reachability_graph, environment, matplotlib=False)
            save_image(image, os.path.dirname(__file__) + "/" + agent.name + "/", "seed_" + str(seed_id) + ".png")

            if False and isinstance(agent, SGM):
                plt.imshow(image)
                plt.show()

        if len(episodes_results) > 20:
            print("Episode ", episode_id, ", result = ", episodes_results[-1], ", last 20 episodes average result = ",
                  running_average, sep='', end = "\r")
        else:
            print("Episode ", episode_id, ", result = ", episodes_results[-1], ", last episodes average result = ",
                  running_average, sep='', end = "\r")

        # show_q_value(environment, agent, episode_id)

    #if isinstance(agent, SGM):
    #    plot_graph_on_environment(agent.reachability_graph, environment)
    #    plt.show()

    print(end="\x1b[2K")
    print("Global results: ")
    print(results_running_average[-20:])
    return results_running_average

if __name__ == "__main__":
    nb_seeds = 1
    nb_episodes = 600
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    environment = GoalConditionedDiscreteGridWorld(map_name=MapsIndex.FOUR_ROOMS.value)
    # environment = GoalConditionedPointEnv(map_name=MapsIndex.EMPTY.value, dense_reward=False)

    hl_agent = TILO(DDPG, environment.state_space, environment.action_space)
    control_agent = TILO(SAC, environment.state_space, environment.action_space)
    agents = [
        # HRL(control_agent, 2, hl_agent, planning_horizon=5),
        # TILO(DQN, state_space=environment.state_space, action_space=environment.action_space),
        # HER(DQN, state_space=environment.state_space, action_space=environment.action_space),
        HER(DistributionalDQN, state_space=environment.state_space, action_space=environment.action_space),
        # TILO(SAC, state_space=environment.state_space, action_space=environment.action_space),
        # HRL(control_agent, 2, hl_agent, planning_horizon=15),
    ]

    # Plot results
    results = {}
    for agent in agents:
        results[agent.name] = []

    for seed_id in range(nb_seeds):
        for agent in agents:
            nb_interactions_per_episode = 20 if isinstance(agent, SORB) else 100

            results[agent.name].append(
                get_score(agent, environment, nb_episodes=nb_episodes,
                          nb_interactions_per_episode=nb_interactions_per_episode)
            )
            agent.reset()

    colors = ['#aa381e', '#766ec8', '#e1a95f', '#8fd400', '#4d5d53', '#5b92e5', "#3E757A", "#583D80", "#826F39", "#34778A"]
    for color, agent in zip(colors, agents):
        data = np.array(results[agent.name])
        abscissa = [i for i in range(data.shape[1])]
        data_mean = np.mean(data, 0)
        data_std = np.std(data, 0)

        plt.plot(abscissa, data_mean, c=color, label=agent.name)
        plt.fill_between(abscissa, data_mean + data_std, data_mean - data_std, color=color, alpha=0.1)
    plt.legend()
    plt.show()