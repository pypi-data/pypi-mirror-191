import os
from os.path import isdir
from statistics import mean

from matplotlib import pyplot as plt

from hbrl.agents import GoalConditionedValueBasedAgent, DistributionalDQN, HER
from hbrl.environments import GoalConditionedDiscreteGridWorld, MapsIndex
from hbrl.utils import empty_dir, generate_video


def pre_train(agent: GoalConditionedValueBasedAgent, environment,
              pre_training_duration=300, episode_duration=100):

    results = []
    results_running_average = []
    for episode_id in range(pre_training_duration):
        if episode_id % 10 == 0:
            print("pre training episode ", episode_id)
        results.append(0)
        state, goal = environment.reset()
        agent.start_episode(state, goal)
        for interaction_id in range(episode_duration):
            action = agent.action(state)
            state, reward, done = environment.step(action)
            agent.process_interaction(action, reward, state, done, learn=True)
            if reward == 0:
                results[-1] = 1
                break
        agent.stop_episode()
        if len(results) >= 20:
            results_running_average.append(mean(results[-20:]))

    output_directory = os.path.dirname(__file__) + "/" + agent.name + "_save/"
    agent.save(output_directory)

    print("PRE-TRAIN DONE")
    print("running_average_results = ", results_running_average)
    plt.plot(results_running_average, label=agent.name + " pre training accuracy")
    plt.legend()
    plt.show()
    return results_running_average


def eval_agent(agent, environment, eval_duration=100, eval_episodes_duration=100, load=True):

    if load:
        output_directory = os.path.dirname(__file__) + "/" + agent.name + "_save/"
        agent.load(output_directory)

    video = False
    video_outputs_dir = os.path.dirname(__file__) + "/evaluation_videos/"
    if video and isdir(video_outputs_dir):
        empty_dir(video_outputs_dir)
    results = []
    for episode_id in range(eval_duration):
        results.append(0)
        state, goal = environment.reset()
        agent.start_episode(state, goal, test_episode=True)
        if video:
            images = []

        if video:
            image = environment.render()
            images.append(image)

        for interaction_id in range(eval_episodes_duration):
            action = agent.action(state)
            state, reward, done = environment.step(action)
            agent.process_interaction(action, reward, state, done, learn=False)
            if video:
                image = environment.render()
                images.append(image)
            if reward == 0:
                results[-1] = 1
                break
        agent.stop_episode()
        if video:
            generate_video(images, video_outputs_dir, "episode_" + str(episode_id))
    print("EVAL DONE")
    print("evaluation_grade = ", mean(results))
    return results



if __name__ == "__main__":

    environment = GoalConditionedDiscreteGridWorld(map_name=MapsIndex.FOUR_ROOMS.value)
    # environment = GoalConditionedPointEnv()
    nb_seeds = 1
    for seed_id in range(nb_seeds):
        agent = HER(DistributionalDQN, state_space=environment.state_space, action_space=environment.action_space, nb_models=3)
        # agent = HER(DQN, state_space=environment.state_space, action_space=environment.action_space)
        # agent = TILO(DQN, state_space=environment.state_space, action_space=environment.action_space)
        # agent = HER(SAC, state_space=environment.state_space, action_space=environment.action_space)
        # agent = HER(DistributionalDDPG, state_space=environment.state_space, action_space=environment.action_space)

        # pre_train(agent, environment)
        evaluation(agent, environment)

        for model_id in range(agent.nb_models):
            plt.plot(agent.errors["model_" + str(model_id)], label="loss model " + str(model_id))
        plt.legend()
        plt.show()

        agent.reset()