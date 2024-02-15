import torch
import random
import numpy as np
from collections import deque
from Uno_RL import Deck,Player,startGame
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY =100_000
BATCH_SIZE =1000
LR =0.001

class Agent:

    def __init__(self):
        self.n_games=0
        self.epsilon=0 # controls randomness
        self.gamma =0.9  # discount rate - has to be smaller than 1
        self.memory =deque(maxlen=MAX_MEMORY) #call pop left for us
        self.model= Linear_QNet(11,256,3)# input, hidden and output size
        self.trainer=QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state (self, startGame):
        pass
        #bring in code for discard card
        #bring in code for the hand
        #state=[list of 11 states
            #have to pick_up
            #won
            #lost
            #wild_card avaialble
            # check for playable_card against played card]
        state=[

        ]
        #convert list to numpy array
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))# pop left if max memory is reached

    def train_long_memory(self):
        if len(self.memory)> BATCH_SIZE:
            mini_sample= random.sample(self.memory, BATCH_SIZE)# returns a list of tuples
        else:
            mini_sample=self.memory
        #use python built in zip function to group together the states, actions, rewards etc
        #could also have been done with a for loop
        states, actions, rewards, next_states, dones = zip(*mini_sample) 
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)



    def get_action(self, state):
    #random moves:tradeoff between exploration (PC random)/exploitation( AI learning) - we use epsilon
        self.epsilon = 80- self.n_games
        final_move=[0,0,0]
        if random.randint(0,200)< self.epsilon:
            move= random.randint(0,2)# 2 is included
            final_move[move]=1
    #the more games, the smaller epsilon will get. the smaller the epsilon, the less chance randint willl be less than epsilon
    #it can get to negative numbers which means, the moves are no longer random
        else:
        #we want a move based on our model. It wats to predict based on 1 state (state0)
        #convert state to a tensor
            state0=torch.tensor(state, dtype=torch.float)
            prediction =self.model(state0)
        #convert from raw number to 1 hot encoded value
            move =torch.argmax(prediction).item()
            final_move[move]=1
        return final_move    

def train():
    plot_scores=[]
    plot_mean_scores=[]
    total_score =0
    record =0
    agent = Agent()
    game = startGame()
    while True:
        #get the old state
        state_old = agent.get_state(startGame)
        #get move
        final_move =agent.get_action(state_old)

        #perform move and get new state
        reward, done, score = startGame.play_step(final_move)
        state_new = agent.get_state(startGame)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #train the long memory, plot results
            startGame.reset()
            agent.n_games=+1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game',agent.n_games, 'Score', score, 'Record',record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores,plot_mean_scores)





if __name__ == '__main__':
    train()