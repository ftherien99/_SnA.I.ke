import random
from os import path

import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim

from QNetwork import QNetwork
from ReplayBuffer import ReplayBuffer

#INSPIRATIONS: https://youtu.be/wc-FxNENg9U et dqn_agent.py dans la section References/DQL exemple dans le git

class Agent:

    def __init__(self,inputDims, numberOfActions, seed, qNetworkPath):
        if torch.cuda.is_available:
            self.device = torch.device("cuda:0") #carte graphique
        else:
            self.device = torch.device("cpu")

        self.bufferSize = int(1e5)
        self.batchSize = 64
        self.gamma = 0.99
        self.tau = 1e-3
        self.learningRate = 5e-4 
        self.updateNetwork = 4
        self.inputDims = inputDims #state size
        self.numberOfActions = numberOfActions
        self.seed = random.seed(seed)
        self.qNetworkPath = qNetworkPath

        

        if path.exists(self.qNetworkPath): #Va prendre le qNetowrk entraine

            self.qNetworkLocal = QNetwork(self.inputDims, self.numberOfActions, seed,64,64).to(self.device)
            self.qNetworkLocal.load_state_dict(torch.load(self.qNetworkPath))
            self.qNetworkLocal.eval()

            self.qNetworkTarget = QNetwork(self.inputDims, self.numberOfActions, seed, 64,64).to(self.device)
            self.qNetworkTarget.load_state_dict(torch.load(self.qNetworkPath))
            self.qNetworkTarget.eval()
        else:
            self.qNetworkLocal = QNetwork(self.inputDims, self.numberOfActions, seed,64,64).to(self.device)
            self.qNetworkTarget = QNetwork(self.inputDims, self.numberOfActions, seed, 64,64).to(self.device)


        
        self.optimizer = optim.Adam(self.qNetworkLocal.parameters(), self.learningRate)

        self.agentMemory = ReplayBuffer(self.numberOfActions, self.bufferSize, self.batchSize, seed)
        self.timesteps = 0
     



    def step(self, state, action, reward, nextState, isDone):
        #isDone = is the game over
        self.agentMemory.addExperience(state,action,reward,nextState,isDone)

        self.timesteps = (self.timesteps + 1) % self.updateNetwork

        #sert a apprendre apres un certains nombre de temps
        if self.timesteps == 0:
            if len(self.agentMemory.memory) > self.batchSize:
                experiences = self.agentMemory.sampleExperience()
                self.learn(experiences, self.gamma)


    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.qNetworkLocal.eval() # dit au QNetwork de faire une evaluation

        with torch.no_grad():
            actionValues = self.qNetworkLocal.forward(state)
        self.qNetworkLocal.train()
    
        action =  np.argmax(actionValues.cpu().data.numpy())
            
        return action


    def learn(self, experiences, gamma):
       
        states, actions, rewards, nextStates, isDones = experiences

        qTargetNext = self.qNetworkTarget(nextStates).detach().max(1)[0].unsqueeze(1)

        qTarget = rewards + (gamma * qTargetNext * (1 - isDones))

        qValue = self.qNetworkLocal(states).gather(1,actions)

        loss = F.mse_loss(qValue, qTarget)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


        self.targetQNetworkUpdate(self.qNetworkLocal, self.qNetworkTarget, self.tau)


        

    def targetQNetworkUpdate(self, qNetworkLocal, qNetworkTarget, tau):
        for targetParams, localParams in zip(qNetworkTarget.parameters(), qNetworkLocal.parameters()):
            targetParams.data.copy_(tau*localParams.data + (1.0-tau)*targetParams.data)
