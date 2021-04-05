class Agent:
    def __init__(self):
        self.bufferSize = 0
        self.batchSize = 0
        self.gamma = 0.0
        self.tau = 0.0
        self.learningRate = 0.0
        self.updateNetwork = 0
        self.stateSize = 0
        self.actionSize = 0
        #self.speed = 0
        #self.qNetworkLocal = QNetwork()
        #self.qNetworkTarget = QNetwork()
        #self.agentMemory = ReplayBuffer()



    def step(self, state, action, reward, nextState, isDone):
        pass


    def act(self, state, epsilon):
        pass


    def learn(self, experiences, gamma):
        pass

    def targetQNetworkUpdate(self, qNetworkLocal, qNetworkTarget, tau):
        pass
