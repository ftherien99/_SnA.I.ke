import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#INSPIRATIONS: https://youtu.be/wc-FxNENg9U et model.py dans la section References/DQL exemple dans le git


class QNetwork(nn.Module):

    def __init__(self, learningRate, inputDims, layer1Dims, layer2Dims, numberOfActions):
        super(QNetwork, self).__init__()

        #INPUT DIMS = STATE
        #inputDims[0] = posX
        #inputDims[1] = posY
        #inputDims[2] = bodyLength
        #inputDims[4] = contact with apple (1 if yes, 0 if not)
        
        #NUMBER OF NEURONS
        self.inputDims = inputDims
        self.layer1Dims = layer1Dims
        self.layer2Dims = layer2Dims

        self.numberOfActions = numberOfActions
        self.learningRate = learningRate

        #LAYERS
        self.layer1 = nn.Linear(self.inputDims,self.layer1Dims)
        self.layer2 = nn.Linear(self.layer1Dims, self.layer2Dims)
        self.layer3 = nn.Linear(self.layer2Dims, self.numberOfActions)

        self.optimizer = optim.Adam(self.parameters(), lr = self.learningRate)
        self.loss = nn.MSELoss()
        
        if torch.cuda.is_available():
            print("YES YES YES")
            self.device = torch.device("cuda:0") #GPU
        else:
            self.device = torch.device("cpu")

        self.to(self.device)



    def forward(self, state):
        x = F.relu(self.layer1(state))
        x = F.relu(self.layer2(x))
        action = F.relu(self.layer3(x))
        return action