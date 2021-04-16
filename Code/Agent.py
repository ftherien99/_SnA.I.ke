from QNetwork import QNetwork
from ReplayBuffer import ReplayBuffer
import torch
import torch.nn.functional as F
import numpy as np
import random
import torch.optim as optim
from os import path

class Agent:

    def __init__(self,inputDims, numberOfActions, seed):
        if torch.cuda.is_available:
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

        self.bufferSize = int(1e5)
        self.batchSize = 64 ###
        self.gamma = 0.99
        self.tau = 1e-3
        self.learningRate = 5e-4 
        self.updateNetwork = 4
        self.inputDims = inputDims #state size = 4
        self.numberOfActions = numberOfActions
        self.seed = random.seed(seed)

        if path.exists("qNetwork.pth"): #Va prendre le qNetowrk entraine
            self.qNetworkLocal = QNetwork(self.inputDims, self.numberOfActions, seed,64,64).to(self.device)
            self.qNetworkLocal.load_state_dict(torch.load("qNetwork.pth"))
            self.qNetworkLocal.eval()
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


    def act(self, state, epsilon = 0.):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.qNetworkLocal.eval() # dit au QNetwork de faire une evaluation

        with torch.no_grad():
            actionValues = self.qNetworkLocal.forward(state)
        self.qNetworkLocal.train()

        if random.random() > epsilon: #Si on depasse epsilon, faire une action ''greedy'', sinon faire une action random
            action =  np.argmax(actionValues.cpu().data.numpy())
            
        else:
            action = random.choice(np.arange(self.numberOfActions))
            

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