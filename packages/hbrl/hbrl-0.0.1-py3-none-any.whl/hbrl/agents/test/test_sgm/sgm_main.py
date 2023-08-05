import os
from os.path import isdir
from statistics import mean

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from hbrl.agents import SGM, HER
from hbrl.agents.test.test_sgm.pre_train_agent import pre_train, evaluation
from hbrl.environments import plot_graph_on_environment, GoalConditionedDiscreteGridWorld, MapsIndex
from hbrl.utils import save_image, generate_video, empty_dir


def sgm_main(nb_pruning_episode=300, pruning_episodes_duration=100):
    pre_training = False
    environment = GoalConditionedDiscreteGridWorld(map_name=MapsIndex.FOUR_ROOMS.value)
    agent = SGM(agent_wrapper=HER, state_space=environment.state_space, action_space=environment.action_space,
                max_edges_length=5, node_pruning_threshold=2,
                reachability_threshold=environment.reachability_threshold, nb_models=3)
    pre_train_results = []
    if pre_training:
        pre_train_results = pre_train(agent.control_policy, environment, pre_training_duration=500)
        eval_results = evaluation(agent.control_policy, environment)
    else:
        output_directory = os.path.dirname(__file__) + "/" + agent.control_policy.name + "_save/"
        agent.control_policy.load(output_directory)
        eval_results = evaluation(agent.control_policy, environment)
    agent.build_graph()
    image = plot_graph_on_environment(agent.reachability_graph, environment, matplotlib=False)
    save_image(image, os.path.dirname(__file__) + "/", "sgm_graph.png")
    image = plot_graph_on_environment(agent.reachability_graph, environment, matplotlib=False, nodes_only=True)
    save_image(image, os.path.dirname(__file__) + "/", "sgm_nodes.png")
    results = []
    results_running_average = []
    video = True
    if video and isdir(os.path.dirname(__file__) + "/videos/"):
        empty_dir(os.path.dirname(__file__) + "/videos/")
    for episode_id in range(nb_pruning_episode):
        if episode_id % 10 == 0:
            print("pruning episode " + str(episode_id))
            print("results_running_average = ", results_running_average)
        state, goal = environment.reset()
        agent.start_episode(state, goal)
        results.append(0)
        if video:
            images = []
            image = environment.render()
            for sub_goal in agent.sub_goals:
                sg = nx.get_node_attributes(agent.reachability_graph, "state")[sub_goal] \
                    if isinstance(sub_goal, int) else sub_goal.copy()
                assert isinstance(sg, np.ndarray)
                image = environment.place_point(image, sg, [196, 146, 29])
            image = environment.place_point(image, agent.control_policy.current_goal, [255, 0, 0])
            images.append(image)
        for interaction_id in range(pruning_episodes_duration):
            action = agent.action(state)
            state, reward, done = environment.step(action)
            agent.process_interaction(action, reward, state, done, learn=True)
            if video:
                image = environment.render()
                for sub_goal in agent.sub_goals:
                    sg = nx.get_node_attributes(agent.reachability_graph, "state")[sub_goal] \
                        if isinstance(sub_goal, int) else sub_goal.copy()
                    assert isinstance(sg, np.ndarray)
                    image = environment.place_point(image, sg, [196, 146, 29])
                image = environment.place_point(image, agent.control_policy.current_goal, [255, 0, 0])
                images.append(image)
            if reward == 0:
                results[-1] = 1
                break
        if video:
            generate_video(images, os.path.dirname(__file__) + "/videos/", "episode_" + str(episode_id))

        if len(results) >= 20:
            results_running_average.append(mean(results[-20:]))
    print("results_running_average = ", results_running_average)
    plt.plot(pre_train_results, label="pre_train")
    plt.plot(eval_results, label="eval_results")
    plt.plot(results_running_average, label="pruning_results")
    plt.axhline(y=mean(eval_results), color='r', linestyle='-', label="average evaluation result")
    plt.legend()
    plt.show()

if __name__ == "__main__":

    sgm_main()