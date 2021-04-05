import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#INSPIRATIONS: https://youtu.be/wc-FxNENg9U et model.py dans la section References/DQL exemple dans le git


class QNetwork(nn.Module):

    def __init__(self, learningRate, actionDims, fc1Dims, fc2Dims, numberOfActions):
        super(QNetwork, self).__init__()

        #NUMBER OF NEURONS
        self.actionDims = actionDims
        self.fc1Dims = fc1Dims
        self.fc2Dims = fc2Dims

        self.numberOfActions = numberOfActions
        self.learningRate = learningRate

        #LAYERS
        self.fc1 = nn.Linear(self.actionDims,self.fc1Dims)
        self.fc2 = nn.Linear(self.fc1Dims, self.fc2Dims)
        self.fc3 = nn.Linear(self.fc2Dims, self.numberOfActions)

        self.optimizer = optim.Adam(self.parameters(), lr = self.learningRate)
        self.loss = nn.MSELoss()
        
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

        self.to(self.device)



    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        action = F.relu(self.fc3(x))
        return action