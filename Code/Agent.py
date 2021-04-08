from QNetwork import QNetwork
from ReplayBuffer import ReplayBuffer
import torch
import numpy as np
import random

class Agent:

    def __init__(self, bufferSize, batchSize, gamma, epsilon, epsilonMin = 0.01, epsilonDecr = 5e-4, tau, learningRate, updateNetwork, inputDims, numberOfActions, boards):
        self.bufferSize = bufferSize
        self.batchSize = batchSize
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonMin = epsilonMin
        self.tau = tau
        self.learningRate = learningRate
        self.updateNetwork = updateNetwork
        self.inputDims = inputDims #state size = 4
        self.numberOfActions = numberOfActions
        #self.speed = 0
        self.qNetworkLocal = QNetwork(self.learningRate, self.inputDims, 256, 256, self.numberOfActions)
        self.qNetworkTarget = QNetwork(self.learningRate, self.inputDims, 256, 256, self.numberOfActions)
        self.agentMemory = ReplayBuffer(self.bufferSize, self.batchSize)
        self.timesteps = 0
        self.actionSpace = [i for in range(self.numberOfActions)]
        self.boards = boards



    def step(self, state, action, reward, nextState, isDone):
        #isDone = is the game over
        self.agentMemory.addExperience(state,action,reward,nextState,isDone)

        self.timesteps = (self.timesteps + 1) % self.updateNetwork

        #sert a apprendre apres un certains nombre de temps
        if self.timesteps == 0:
            if len(self.agentMemory.memory) > self.batchSize:
                experiences = self.agentMemory.sampleExperience()
                self.learn(experiences, self.gamma)


    def act(self, state, epsilon):
        state = torch.from_numpy(state).float.unsqueeze(0).to(self.qNetworkLocal.device)
        self.qNetworkLocal.eval() # dit au QNetwork de faire une evaluation

        with torch.no_grad():
            actionValues = self.qNetworkLocal.forward(state)

        if random.random() > epsilon: #Si on depasse epsilon, faire une action ''greedy'', sinon faire une action random
            action =  np.argmax(actionValues.cpu().data.numpy())
        else:
            action =  random.choice(np.arange(self.numberOfActions))

        return action


    def learn(self, experiences, gamma):
        states, actions, rewards, nextStates, isDones = experiences

        qTargetNext = self.qNetworkTarget(nextStates).detach().max(1)[0].unsqueeze(1)

        qTarget = rewards + (gamma * qTargetNext * (1 - isDones))

        qValue = self.qNetworkLocal(states).gather(1,actions)

        loss = F.mse_loss(qValue, qTarget)

        self.qNetworkLocal.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.targetQNetworkUpdate(self.qNetworkLocal, self.qNetworkTarget, self.tau)

        

    def targetQNetworkUpdate(self, qNetworkLocal, qNetworkTarget, tau):
        for targetParams, localParams in zip(qNetworkTarget.parameters(), qNetworkLocal.parameters()):
            targetParams.data.copy_(tau*localParams.data + (1.0-tau)*targetParams.data)