import torch, random
import numpy as np
from collections import deque
from SnakeGameAI import Snake, Direction
from model import Linear_QNet, QTrainer
from plot import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.game_count = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate (must be smaller than one)
        self.memory = deque(maxlen=MAX_MEMORY) # will popleft() if grows too large
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr= LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        # points in all directions to determine if approaching wall
        head = game.snake_head
        # 25 being the size of snake block constant
        point_left = [head[0] - 25, head[1]]
        point_right = [head[0] + 25, head[1]]
        point_up = [head[0], head[1] - 25]
        point_down = [head[0], head[1] + 25]

        direction_left = game.direction == Direction.LEFT
        direction_right = game.direction == Direction.RIGHT
        direction_up = game.direction == Direction.UP
        direction_down = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (direction_right and game.check_collision(point_right)) or 
            (direction_left and game.check_collision(point_left)) or 
            (direction_up and game.check_collision(point_up)) or 
            (direction_down and game.check_collision(point_down)),

            # Danger right
            (direction_up and game.check_collision(point_right)) or 
            (direction_down and game.check_collision(point_left)) or 
            (direction_left and game.check_collision(point_up)) or 
            (direction_right and game.check_collision(point_down)),

            # Danger left
            (direction_down and game.check_collision(point_right)) or 
            (direction_up and game.check_collision(point_left)) or 
            (direction_right and game.check_collision(point_up)) or 
            (direction_left and game.check_collision(point_down)),
            
            # Move direction, result of boolean checks above, only one direction will have True
            direction_left,
            direction_right,
            direction_up,
            direction_down,
            
            # Food location 
            game.apple_x < head[0],  # food left
            game.apple_x > head[0],  # food right
            game.apple_y < head[1],  # food up
            game.apple_y > head[1]  # food down
            ]
        #print(np.array(state, dtype=int))
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY limit occurs

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples 
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # as game continues, epsilon continues to shrink, decreasing chances of randomness
        self.epsilon = 80 - self.game_count
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            # make random move in one direction by setting a random index to one
            move = random.randint(0,2)
            final_move[move] = 1

        else:
            # best action selected by neural network
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # select move with highest value
            move = torch.argmax(prediction).item()
            # set cooresponding index to 1 to move in that direction
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Snake()
    while True:
        # get old state
        current_state = agent.get_state(game)

        # get move
        final_move = agent.get_action(current_state)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory, current state
        agent.train_short_memory(current_state, final_move, reward, state_new, done)

        # remember (add current state to deque)
        agent.remember(current_state, final_move, reward, state_new, done)

        if done: # game over
            # train long memory and plot outcome
            game.reset()
            agent.game_count +=1
            # train neural network with all actions taken 
            agent.train_long_memory()

            # check for new top score
            if score > record:
                record = score
                agent.model.save()

            # print game count, with current game's score, and the best score achieved overall
            print(f"Game {agent.game_count} Score {score} Record {record}")

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.game_count
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()