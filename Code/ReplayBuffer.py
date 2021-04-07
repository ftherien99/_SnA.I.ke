from collections import deque
import numpy as np
import torch
class ReplayBuffer:
    def __init__(self,bufferSize, batchSize):
        self.bufferSize = bufferSize
        self.batchSize = batchSize
        self.memory = deque(maxlen=self.bufferSize)
        self.experience = namedtuple("Experience", field_names=["state","action","reward","nextState","isDone"])


    def addExperience(self,state, action, reward, nextState, isDone):
        experience = self.experience(state,action,reward,nextState,isDone)
        self.memory.append(experience)



    def sampleExperience(self):
        experiences = random.sample(self.memory, k = self.batchSize)
        #torch.from_numpy: retourne un tensor
        #np.vstack: retourne un ndarray (plusieurs array mis en ligne)
        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        nextStates = torch.from_numpy(np.vstack([e.nextState for e in experiences if e is not None])).float().to(device)
        #isDones = torch.from_numpy(np.vstack([e.isDone for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
        return (states,actions,rewards,nextStates)