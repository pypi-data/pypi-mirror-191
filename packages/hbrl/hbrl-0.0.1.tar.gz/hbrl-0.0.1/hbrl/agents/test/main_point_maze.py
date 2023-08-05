import os.path
from copy import deepcopy

import numpy as np
# import optuna.exceptions
import torch.cuda
from statistics import mean
from hbrl.agents.global_planning.reachability_graph_learning.sgm import SGM
from hbrl.environments import plot_graph_on_environment, GoalConditionedDiscreteGridWorld
from hbrl.agents.global_planning.reachability_graph_learning.sorb import SORB
from hbrl.environments.point_env.goal_conditioned_point_env import GoalConditionedPointEnv
import matplotlib.pyplot as plt
from hbrl.utils import get_red_green_color, save_image, generate_video
from hbrl.agents.goal_conditioned_wrappers.her import HER
from hbrl.agents.agent import Agent
from hbrl.environments import MapsIndex
import networkx as nx


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


def get_score(agent: Agent, environment, pre_train_episodes, pruning_episodes, nb_interactions_per_episode, trial=None):
    episodes_before_video = 5
    episodes_before_graph_img = 10
    running_episode_results_average = []
    episodes_results = []
    if episodes_before_video is not None:
        output_dir = os.path.dirname(__file__) + "/videos/"

    load = True
    start_episode = pre_train_episodes if load else 0
    if load:
        agent.control_policy.reinforcement_learning_agent.load(os.path.dirname(__file__) + "/control_policy_save/")
    for episode_id in range(start_episode, pre_train_episodes + pruning_episodes):
        graph_navigation = isinstance(agent, SORB) and agent.graph_up_to_date
        episodes_results.append(0)
        state, goal = environment.reset()
        agent.start_episode(state, goal)
        interaction_id = 0
        if graph_navigation:
            image = environment.render()
            if isinstance(agent, SORB) and agent.sub_goals:
                for sub_goal in agent.sub_goals:
                    sg = nx.get_node_attributes(agent.reachability_graph, "state")[sub_goal] \
                        if isinstance(sub_goal, int) else sub_goal.copy()
                    assert isinstance(sg, np.ndarray)
                    image = environment.place_point(image, sg, [196, 146, 29])
                image = environment.place_point(image, agent.control_policy.current_goal, [255, 0, 0])
            images = [image]
        while True:
            action = agent.action(state)
            state, reward, done = environment.step(action)
            agent.process_interaction(action, reward, state, done)
            if graph_navigation:
                image = environment.render()
                if (isinstance(agent, SORB) or isinstance(agent, SGM)) and agent.sub_goals:
                    for sub_goal in agent.sub_goals:
                        sg = nx.get_node_attributes(agent.reachability_graph, "state")[sub_goal] \
                            if isinstance(sub_goal, int) else sub_goal.copy()
                        assert isinstance(sg, np.ndarray)
                        image = environment.place_point(image, sg, [196, 146, 29])
                    assert (agent.next_goal == agent.control_policy.current_goal).all()
                    image = environment.place_point(image, agent.next_goal, [0, 0, 255])

                images.append(image)
            if done:
                episodes_results[-1] = 1
                break
            interaction_id += 1
            if (not graph_navigation and interaction_id == nb_interactions_per_episode) \
                    or (graph_navigation and agent.done):
                if episode_id > 2100:
                    a = 1
                break

        if episodes_before_graph_img is not None and episode_id % episodes_before_graph_img == 0 and graph_navigation:
            image = plot_graph_on_environment(agent.reachability_graph, environment, matplotlib=False)
            save_image(image, os.path.dirname(__file__) + "/" + agent.name + "/", "seed_" + str(seed_id) + "_episode_"
                       + str(episode_id) + ".png")

        agent.stop_episode()
        if graph_navigation and ((episodes_before_video is not None and episode_id % episodes_before_video == 0) or
                                 episodes_results[-1] == 0):
            generate_video(images, output_dir, "episode_" + str(episode_id))
        running_average = mean(episodes_results[-20:] if len(episodes_results) > 20 else episodes_results)
        if isinstance(agent, SORB) and episode_id == pre_train_episodes:
            agent.control_policy.save(os.path.dirname(__file__) + "/control_policy_save/")
            image = environment.render()
            buffer_size = agent.control_policy.reinforcement_learning_agent.replay_buffer.data_size
            states = agent.control_policy.reinforcement_learning_agent.replay_buffer \
                    .sample(buffer_size)[0][:, :2].detach().cpu().numpy()
            for s in states:
                environment.place_point(image, s, [0, 255, 0])

            save_image(image, os.path.dirname(__file__), "/sgm_states.mp4")


            agent.build_graph()
            # Plot agent graph
            image = plot_graph_on_environment(agent.reachability_graph, environment, matplotlib=False)
            save_image(image, os.path.dirname(__file__) + "/" + agent.name + "/", "seed_" + str(seed_id) + ".png")

            if False and isinstance(agent, SGM):
                plt.imshow(image)
                plt.show()

        running_episode_results_average.append(running_average)
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
    print(running_episode_results_average[-20:])
    return running_episode_results_average


if __name__ == "__main__":
    nb_seeds = 1
    pre_train_episodes = 500
    pruning_episodes = 500
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # environment = GoalConditionedDiscreteGridWorld(map_name=MapsIndex.EMPTY.value)
    # environment = GoalConditionedPointEnv(map_name=MapsIndex.EMPTY.value, dense_reward=False)
    # environment = GoalConditionedDiscreteGridWorld()
    # environment = GoalConditionedPointEnv(map_name=MapsIndex.FOUR_ROOMS.value, dense_reward=False)
    environment = GoalConditionedDiscreteGridWorld(map_name=MapsIndex.FOUR_ROOMS.value)

    agents = [
        # TILO(SAC, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # HER(SAC, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # TILO(DDPG, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # HER(DDPG, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # HER(DistributionalDDPG, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),

        # TILO(SAC, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),
        # HER(DQN, state_space=environment.state_space, action_space=environment.action_space, device=device),
        SGM(agent_wrapper=HER, state_space=environment.state_space, action_space=environment.action_space,
            device=device, max_edges_length=4, node_pruning_threshold=2,
            reachability_threshold=environment.reachability_threshold, nb_models=1),
        # HER(DistributionalDDPG, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),
        # SORB(agent_wrapper=HER, state_space=environment.state_space, action_space=environment.action_space,
        #      device=device),
        # SORB2(agent_wrapper=HER, state_space=environment.state_space, action_space=environment.action_space,
        #      device=device),
        # HER(DistributionalDDPG, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),
        # HER(DDPG, state_space=environment.state_space, action_space=environment.action_space, device=device),

        # GoalConditionedAgent(SAC, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),

        # HER(SAC, state_space=environment.state_space, action_space=environment.action_space,
        #     device=device),

        # NavigationTilo(DQN, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # HER(DQN, state_space=environment.state_space, action_space=environment.action_space, device=device),
        # GoalConditionedAgent(DQN, state_space=environment.state_space, action_space=environment.action_space,
        #                      device=device)
    ]

    # Plot results
    results = {}
    for agent in agents:
        results[agent.name] = []

    for seed_id in range(nb_seeds):
        for agent in agents:
            nb_interactions_per_episode = 20 if isinstance(agent, SORB) else 100
            nb_interactions_per_episode = 100

            results[agent.name].append(
                get_score(agent, environment, pre_train_episodes, pruning_episodes,
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
    a = 1