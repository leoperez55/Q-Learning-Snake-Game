from agent_based_game import Game, Action
import random
import time

class QLearning:
    def __init__(self, 
                game,
                alpha = 0.5,
                gamma = 0.99,
                epsilon_start = 0.6,
                epsilon_end = 0.01,
                epsilon_decay = 0.003,
                episodes = 1000):
        self.game = game
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.episodes = episodes
        self.Q = {}
        # State space
        self.state_space = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
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

            while not gameover:
                # Epsilon-greedy action selection
                if random.uniform(0, 1) < epsilon:
                    action = random.choice(self.action_space)
                else:
                    action = max(self.action_space, key=lambda a: self.Q[(state, a)])

                # Perform the action and receive the new state, reward, and gameover status
                next_state, reward, gameover, _ = self.game.act(action)
                total_reward += reward

                # Update the Q-value for the current state-action pair using the Q-learning update rule
                old_q_value = self.Q[(state, action)]
                next_q_value = max([self.Q[(next_state, a)] for a in self.action_space])
                self.Q[(state, action)] = old_q_value + self.alpha * (reward + self.gamma * next_q_value - old_q_value)
                state = next_state

            print(f"Episode {episode + 1}/{self.episodes} completed")
            # print(f"Total Reward (Train): {total_reward}")
            # print Q-table
            # for state in state_space:
            #     for action in action_space:
            #         print(f"Q[{state}, {action}]: {Q[(state, action)]}")

            # Decay epsilon to balance exploration and exploitation
            epsilon = max(self.epsilon_end, epsilon * self.epsilon_decay)

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







if __name__ == "__main__":

    game = Game(target_reward=1000)
    agent = QLearning(game)
    agent.train()
    agent.test()