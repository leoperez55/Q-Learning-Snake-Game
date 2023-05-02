from agent_based_game import Game, Action
import numpy as np
import pandas as pd
import random
import time
import os


class QLearning:
    def __init__(
        self,
        game,
        alpha=0.1,
        gamma=0.95,
        epsilon_start=0.6,
        epsilon_end=0.01,
        start_decay_episode=None,
        episodes=1000,
    ):
        self.game = game
        self.alpha = alpha
        self.gamma = gamma
        self.episodes = episodes
        if start_decay_episode is None:
            self.start_decay_episode = episodes // 2
        else:
            self.start_decay_episode = min(episodes - 1, start_decay_episode)
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = (self.epsilon_start - self.epsilon_end) / (
            self.episodes - self.start_decay_episode
        )
        self.Q = {}
        # State space
        self.state_space = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        # Action space
        self.action_space = list(Action)
        self._initializeQTable()

    def _initializeQTable(self):
        # Initialize the Q-table with all zeros
        for state in self.state_space:
            for action in self.action_space:
                self.Q[(state, action)] = 0

    def train(self):
        # Training loop
        epsilon = self.epsilon_start
        for episode in range(self.episodes):
            # visualize every 10 episodes
            # if (episode) % 100 == 0:
            #     game.reset(visualizeNext=True)
            # else:
            #     game.reset()
            self.game.reset(visualizeNext=False)
            gameover = False
            state, _ = self.game.getState()
            total_reward = 0
            score = 0

            while not gameover:
                # Epsilon-greedy action selection
                if random.uniform(0, 1) < epsilon:
                    action = random.choice(self.action_space)
                else:
                    action = max(self.action_space, key=lambda a: self.Q[(state, a)])

                # Perform the action and receive the new state, reward, and gameover status
                next_state, reward, gameover, score = self.game.act(action)
                total_reward += reward

                # Update the Q-value for the current state-action pair using the Q-learning update rule
                old_q_value = self.Q[(state, action)]
                max_future_q_value = max(
                    [self.Q[(next_state, a)] for a in self.action_space]
                )

                new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (
                    reward + self.gamma * max_future_q_value
                )

                self.Q[(state, action)] = new_q_value
                # os.system("cls" if os.name == "nt" else "clear")
                # print(f"Current state: {state}")
                state = next_state
                # print(f"Current action: {action}")
                # self.printQTable()

            print(f"Episode {episode + 1}/{self.episodes} completed")
            # print(f"Score: {score}")
            # print(f"Total Reward (Train): {total_reward}")

            # Decay epsilon to balance exploration and exploitation
            if episode >= self.start_decay_episode:
                epsilon += self.epsilon_decay

    def test(self):
        # Test the trained agent
        self.game.reset(visualizeNext=True)
        gameover = False
        total_reward = 0
        state, _ = game.getState()

        while not gameover:
            action = max(self.action_space, key=lambda a: self.Q[(state, a)])

            state, reward, gameover, _ = self.game.act(action)
            total_reward += reward

        print(f"Total Reward (Test): {total_reward}")
        for state in self.state_space:
            action = max(self.action_space, key=lambda a: self.Q[(state, a)])
            print(f"state: {state}, action: {action}")

    def printQTable(self):
        print(
            pd.DataFrame(
                [
                    [self.Q[(state, action)] for state in self.state_space]
                    for action in self.action_space
                ],
                index=self.action_space,
                columns=self.state_space,
            )
        )


if __name__ == "__main__":
    game = Game(target_reward=10, runtime=5)
    agent = QLearning(game, episodes=3000, alpha=0.5, epsilon_start=0.9)

    agent.printQTable()
    agent.train()
    agent.printQTable()
    while True:
        agent.test()
