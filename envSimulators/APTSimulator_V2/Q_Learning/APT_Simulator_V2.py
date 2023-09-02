#!/usr/bin/env python
# coding: utf-8
import random
import uuid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast


def define_steps_parameters():
    # Define goal and desired steps
    goal = 549
    desired_steps = [597, 1157]


def load_dataset()
    # Read the CSV file into a pandas DataFrame
    abilities_df = pd.read_csv(f"param_req_{platform.upper()}.csv")

    # Set the display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)

    # Display the DataFrame
    abilities_df

    # Update executors_sources column
    abilities_df['executors_sources'] = abilities_df['executors_sources'].apply(ast.literal_eval)
    # Update requirements_sources column
    abilities_df['requirements_sources'] = abilities_df['requirements_sources'].apply(ast.literal_eval)


def define_model _behaviour():
    # Train the model using deep Q-learning
    num_episodes_limit = 10
    num_episodes = 10*num_episodes_limit
    max_steps_per_episode = 10
    learning_rate = 0.9
    discount_rate = 0.95
    exploration_rate = 1
    max_exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 3/num_episodes_limit


def plot_explotarion_rate_function():
    # Create an array of episode numbers
    episodes = np.arange(num_episodes_limit*2)

    # Calculate the exploration rate for each episode
    exploration_rates = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episodes)

    # Plot the exploration rate
    plt.plot(episodes, exploration_rates)
    plt.xlabel('Episode')
    plt.ylabel('Exploration Rate')
    plt.title('Exploration Rate Decay')
    plt.grid(True)
    plt.show(block=False)


def initialize_enviromnent():
    # Define a dictionary to store the unlocked parameters for each step
    unlocked_params = {}
    abilities_run = {}

    # Initialize the first step and its unlocked parameters
    current_episode = 0
    unlocked_params = [[] for _ in range(num_episodes+1)]
    unlocked_params[current_episode] = []
    total_rewards = []
    total_reward = 0
    abilities_run[current_episode] = []


def execute_ability(ability, unlocked_params):
    # Check if all required parameters have been unlocked for this step
    print()
    print("Ability: ", ability)
    required_params = abilities_df.loc[ability, 'requirements_sources']
    
    # Append unlocked parameters for this ability
    current_abilities_run = abilities_run[current_episode]
    previous_ability = current_abilities_run[-1]
    required_params_prev = abilities_df.loc[previous_ability, 'requirements_sources']
    unlocked_params_ability = abilities_df.loc[ability, 'executors_sources']
    current_abilities_run.append(ability)
    
    unlocked_params[current_episode] += [str(param) for param in abilities_df.loc[ability, 'executors_sources'] if str(param) not in unlocked_params[current_episode]]
    print("Unlocked params: ", unlocked_params[current_episode])

    # Check if the objective has been reached
    if len(abilities_run[current_episode]) == max_steps_per_episode:
        initial_ability = abilities_run[current_episode][max_steps_per_episode-1]
        if not abilities_df.loc[initial_ability, 'requirements_sources']:
            return True, 0.3
        return True, -0.3
    elif current_abilities_run.count(ability) > 1:
        return False, -0.5
    elif ability in des_steps:
        des_steps.remove(action)
        return False, 0.5
    elif all(param in unlocked_params_ability for param in required_params_prev) and len(unlocked_params_ability) != 0 and len(required_params_prev) != 0:
        reward = 0.5
        return False, reward
    elif all(param in unlocked_params[current_episode] for param in required_params_prev):
        reward = 0.3
        return False, reward
        
    # Return the result of the ability and a small positive reward
    return False, 0


def add_total_rewards(total_reward):
    total_rewards.append(total_reward)


def is_more_than_once(ability, current_abilities_run):
    count = 0
    for i in current_abilities_run:
        if i == ability:
            count += 1
            if count > 1:
                return True
    return False


def check_valid_next_states(ability, valid_next_states, episode_unlocked_params):
    required_params = abilities_df.loc[ability, 'requirements_sources']
    print(required_params)
    for next_ability in range(action_space):
        unlocked_params = abilities_df.loc[next_ability, 'executors_sources']
        if len(required_params) <= 0:
            valid_next_states.append(next_ability)
        elif len(unlocked_params) > 0:
            for unlocked_param in unlocked_params:
                if unlocked_param in required_params and not unlocked_param in episode_unlocked_params:
                    valid_next_states.append(next_ability)
        
#    print("valid next states: ", valid_next_states)
    return valid_next_states


def run_model():
    # Initialize the Q-table
    action_space = len(abilities_df['ability_id'])
    state_space = len(abilities_df['ability_id'])
    q_table = np.zeros((state_space, action_space))
    np.save('best_q_table.npy', q_table)
    print("Q Table")
    print(q_table)

    # Train the Q-table over a number of steps
    for current_episode in range(num_episodes):
        # Initialize the q_table with values from the best model
        best_q_table = np.load('best_q_table.npy')
        q_table = best_q_table.copy()
        
        # Reset the environment for a new episode
        total_reward = 0
        abilities_run[current_episode] = []
        unlocked_params[current_episode] = []
        current_state = goal
        valid_next_states = []
        valid_next_states = check_valid_next_states(current_state, valid_next_states, unlocked_params[current_episode])
        current_abilities_run = abilities_run[current_episode]
        current_abilities_run.append(current_state)
        des_steps = desired_steps[:]
        
        print("Current episode:", current_episode)
        print("Ability: ", current_state)
        print("Unlocked params: ", abilities_df.loc[current_state, 'executors_sources'])
        print("Success: False - Reward: 0.0")
        
        for step in range(max_steps_per_episode-1):
    #        print("Step: ", step+1)
            # Choose an action using an epsilon-greedy policy
            exploration_rate_threshold = 0
            exploration_rate_threshold = random.uniform(0, 1)
            print("Exploration: ", exploration_rate, "- Exploration threshold: ", exploration_rate_threshold)
            print(q_table[current_state][valid_next_states])
            print("VALID: ", valid_next_states[:10])
            if exploration_rate_threshold > exploration_rate:
                # Exploitation
                print("EXPLOIT")
                q_table_list = q_table[current_state][valid_next_states]
                max_index = np.argmax(q_table_list)
                action = valid_next_states[max_index]
            else:
                # Exploration
                print("EXPLORE")
                if len(des_steps) > 0 and des_steps[-1] in valid_next_states:
                    action = des_steps[-1]
                else:
                    action = random.choice(valid_next_states)
            
            # Execute the selected action (i.e., ability)
            success, reward = execute_ability(action, unlocked_params)
            print(f"Success: {success} - Reward: {reward}")

            # Update the total reward for this episode
            total_reward += reward
            
            # Update the Q-value for the selected action
            old_q_value = q_table[current_state, action]
            next_q_max = np.max(q_table[current_state])
            new_q_value = (1 - learning_rate) * old_q_value + learning_rate * (reward + discount_rate * next_q_max)
            q_table[current_state, action] = new_q_value
            np.save('best_q_table.npy', q_table)
            
            if success == True:
                add_total_rewards(total_reward)
                break

            # Update the current step based on the unlocked parameters
            valid_next_states = []
            check_valid_next_states(action, valid_next_states, unlocked_params[current_episode])
            print("AAA: ", valid_next_states[:10])
            while len(valid_next_states) <= 0:
                print("BBB: ", current_abilities_run)
                current_abilities_run.pop()
                ability = current_abilities_run[len(current_abilities_run)-1]
                step = step - 1
                check_valid_next_states(ability, valid_next_states, unlocked_params[current_episode])
            current_state = np.argmax(q_table[current_state][valid_next_states])
                    
        if len(total_rewards) < current_episode+1:
            add_total_rewards(total_reward)
        
        # Decay the exploration rate for the next episode
        exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * current_episode)
        
        # Select the step with highest value
        if current_episode == 0:
            max_episode_reward = total_reward
            max_episode = 0
        else:
            if total_reward > max_episode_reward:
                max_episode_reward = total_reward
                max_episode = current_episode
            if current_episode >= max_episode+num_episodes_limit:
                break
        
        # Print the total reward for this episode
        print(f"Episode {current_episode} - Total Reward: {total_reward}")
        print("")
        print("Abilities: ", abilities_run[current_episode])
        print("----------------------------------------------------------------------------------------------------------------------------")
    #    print(q_table)

    best_model_list = abilities_run[max_episode][::-1]

    print("")
    print(f"Best Episode: {max_episode} - Maximum Reward: {max_episode_reward}")
    print(f"Unlocked Parameters: {unlocked_params[max_episode]} - Abilities: {best_model_list}")


def genetate_file(model_name, model_UUID, model_description):
    # Write the content to the file
    with open(model_UUID + '.yml', 'w') as f:
        print('---', file = f)
        print('', file = f)
        print('id: ' + model_UUID, file = f)
        print('name: ' + model_name, file = f)
        print('description: ' + model_description, file = f)
        print('atomic_ordering:', file = f)
        for ability in best_model_list:
            print('  - ' + abilities_df.iloc[ability]['ability_id'], file = f)


def plot_fitness_function(current_episode):
    episodes = [i for i in range(0, current_episode+1)]
    error = len(total_rewards)-len(episodes)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    ax1.plot(episodes, total_rewards[:len(total_rewards)-error])
    ax1.set_title("Function Value")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Function Value")

    cumulative_rewards = np.cumsum(total_rewards[:len(total_rewards)-error])

    ax2.plot(episodes, cumulative_rewards)
    ax2.set_title("Accumulated Value")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Accumulated Value")

    plt.show()


def main():
    print("HILA")