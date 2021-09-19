import random
from collections import deque, namedtuple

import numpy as np
import torch

#INSPIRATIONS: dqn_agent.py dans la section References/DQL exemple dans le git

class ReplayBuffer:
    def __init__(self,numberOfActions, bufferSize, batchSize, seed):
        self.numberOfActions = numberOfActions
        self.bufferSize = bufferSize
        self.batchSize = batchSize
        self.memory = deque(maxlen=self.bufferSize)
        self.experience = namedtuple("Experience", field_names=["state","action","reward","nextState","isDone"])
        self.seed = random.seed(seed)
        
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

    def addExperience(self,state, action, reward, nextState, isDone):
        experience = self.experience(state,action,reward,nextState,isDone)
        self.memory.append(experience)



    def sampleExperience(self):
        experiences = random.sample(self.memory, k = self.batchSize)
        #torch.from_numpy: retourne un tensor
        #np.vstack: retourne un ndarray (plusieurs array mis en ligne)
        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(self.device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(self.device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(self.device)
        nextStates = torch.from_numpy(np.vstack([e.nextState for e in experiences if e is not None])).float().to(self.device)
        isDones = torch.from_numpy(np.vstack([e.isDone for e in experiences if e is not None]).astype(np.uint8)).float().to(self.device)

     
        return (states,actions,rewards,nextStates, isDones)
