import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board
from Agent import Agent
from collections import deque
import numpy as np
import torch

class Simulation:
    def __init__(self, main, headColor, bodyColor, appleColor, boardSize, numberOfEpisodes): 
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.appleColor = appleColor
        self.snakeSpeed = 30
        self.boardSize = boardSize
        self.window = self.main.menuWindow
        self.gameSurface = None
        self.score = 0
        self.scoreCheck = 0
        self.board1 = None
        self.board2 = None
        self.board3 = None
        self.board4 = None
        self.isNewHighscore = False
        self.isHighscoreSaved = False
        self.agent = Agent(8, 4, 0)
        self.distance = None
        self.numberOfEpisodes = numberOfEpisodes
        self.startButton = None
        self.resetButton = None
        self.quitButton = None
        

        if self.boardSize == "small":
            self.boardWidth = 1005/2
            self.boardHeight = 605/2
            self.boardArrayX = 50
            self.boardArrayY = 30
            self.boardLeftPadding = 160
            self.boardTopPadding = 85

            #La distance entre chaque board
            self.boardDistanceX = 540
            self.boardDistanceY = 340

            self.highScoreType = "small_board_ai"
        else:
            self.boardWidth = 1205/2
            self.boardHeight = 805/2
            self.boardArrayX = 60
            self.boardArrayY = 40
            self.boardLeftPadding = 40
            self.boardTopPadding = 65

            #La distance entre chaque board
            self.boardDistanceX = 640
            self.boardDistanceY = 440

            self.highScoreType = "large_board_ai"

        self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)

        if self.highscore == None:
            self.highscore = 0


        self.createBoards()
        self.showSimulation()
        
        

    def showSimulation(self):
        buttonX = 850
        buttonY = 1000

        self.window.fill((0,0,0))

        gameBoard1 = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding - 10, self.boardTopPadding - 10, self.boardWidth, self.boardHeight), 2)
        gameBoard2 = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding + self.boardDistanceX, self.boardTopPadding - 10, self.boardWidth, self.boardHeight), 2)
        gameBoard3 = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding - 10, self.boardTopPadding + self.boardDistanceY, self.boardWidth, self.boardHeight), 2)
        gameBoard4 = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding + self.boardDistanceX, self.boardTopPadding + self.boardDistanceY, self.boardWidth, self.boardHeight), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score: " + str(self.score), 1, (0,255,0))
        self.window.blit(scoreText, (100,1025))

        highscoreText = font.render("Highscore: " + str(self.highscore), 1, (0,255,0)) #va aller chercher la valeur dans la bd
        self.window.blit(highscoreText, (375,1025))

        agentRewardText = font.render("Agent Reward:", 1, (0,255,0))
        self.window.blit(agentRewardText, (1300,100))

        episodeText = font.render("Episode:", 1, (0,255,0))
        self.window.blit(episodeText, (1300,175))

        stepsText = font.render("Steps:", 1, (0,255,0))
        self.window.blit(stepsText, (1300,250))

        episodeTimeText = font.render("Episode time (sec):", 1, (0,255,0))
        self.window.blit(episodeTimeText, (1300,325))

        self.startButton = Button(75,225, buttonX, buttonY, (0,255,0), "Start")
        self.startButton.drawButton(self.window)

        self.resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        self.resetButton.drawButton(self.window)

        self.quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        self.quitButton.drawButton(self.window)


        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if self.startButton.clicked(mousePos):
               
                self.deepQLearning()
           
            elif self.quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"

       
    def deepQLearning(self):
        scoreWindow, eps = [], []
        epsilon = 0.9
        epsilonMin = 0.01
        epsilonDecr = 0.995
        episodeCounter = 0
        print(self.numberOfEpisodes)

        for episode in range(self.numberOfEpisodes):
            episodeCounter += 1
            score = 0
            isDone = False
            self.board1 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 8)
            state = self.getState(0)
            for i in range(10000):
                
                for event in pygame.event.get(): #si on clique sur le X
                    if event.type == pygame.QUIT:
                        self.main.snakeDAO.dbCloseConnection()
                        self.main.running = False
                        exit()

                if pygame.mouse.get_pressed() == (1,0,0):
                    mousePos = pygame.mouse.get_pos()

                    if self.quitButton.clicked(mousePos):
                        self.main.currentMenu = "MainMenu"
                        break

                
                action = self.agent.act(state)
                nextState, reward, isDone = self.simulationStep(action)
                self.agent.step(state, action, reward,nextState,isDone)
                state = nextState
                score += reward
                self.board1.tic()
                pygame.display.update()
                if isDone:
                    break

            episodeCounter += 1
            scoreWindow.append(score)
            eps.append(epsilon)
            avgScore = np.mean(scoreWindow[-100:])
            print("episode: ", episode, "  score %.2f " % score, "  average score %.2f:" % avgScore, "  epsilon %.2f" % epsilon)
            epsilon = max(epsilonMin, epsilonDecr * epsilon)

            if episodeCounter == 200:
                torch.save(self.agent.qNetworkLocal.state_dict(), 'qNetwork.pth')
                print("Saving QNetwork")
                episodeCounter = 0
            
            if self.main.currentMenu == "MainMenu":
                break 

            

        


    def createBoards(self):
        self.board1 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 8)
        self.board2 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + self.boardDistanceX + 10, self.boardTopPadding, 8)
        self.board3 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding + self.boardDistanceY + 10, 8)
        self.board4 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + self.boardDistanceX + 10, self.boardTopPadding + self.boardDistanceY + 10, 8)


    def getState(self, appleEaten):
        #vision = self.getSnakeVision()
        #vision = vision.astype('float32')
        #return vision

        left, right, up, down = self.getSnakeVision()

        state = []
        state.append(self.board1.snake.body.deque[0].x)
        state.append(self.board1.snake.body.deque[0].y)
        state.append(self.board1.apple.x)
        state.append(self.board1.apple.y)
        state.append(left)
        state.append(right)
        state.append(up)
        state.append(down)
        state = np.array(state)

        return state

    def simulationStep(self, action):
        reward = 0
        isDone = False
        apple = False
       
        appleX = self.board1.apple.x
        appleY = self.board1.apple.y

        headX = self.board1.snake.body.deque[0].x
        headY = self.board1.snake.body.deque[0].y

        temp = 0

        if self.distance == None:
            self.distance =  ((((headX - appleX)**2) + ((headY - appleY)**2))**0.5)
            
        else:
            temp = ((((headX - appleX)**2) + ((headY - appleY)**2))**0.5)


        if action == 0:
            self.board1.snake.snakeController.changeDirection("up")
        elif action == 1:
            self.board1.snake.snakeController.changeDirection("down")
        elif action == 2:
            self.board1.snake.snakeController.changeDirection("left")
        elif action == 3:
            self.board1.snake.snakeController.changeDirection("right")

       
        if temp < self.distance:
           
            #if temp <= 5:
            #    reward += 2
            #elif temp <= 10:
            #    reward += 1.5
            #elif temp <= 15:
            #    reward += 1
            #elif temp <= 25:
            #    reward += 0.5
            #else:
            #    reward += 0.2

            reward += 0.5
            self.distance = temp
        else:
            
            #if temp <= 5:
            #    reward -= 0.2
            #elif temp <= 10:
            #    reward -= 0.4
            #elif temp <= 15:
            #    reward -= 0.6
            #elif temp <= 25:
            #    reward -= 0.8
            #else:
            #    reward -= 1.2
            reward -= 0.1
            self.distance = temp

        if self.scoreCheck < self.score:
            reward += 30
            self.scoreCheck = self.score
            apple = True

        if self.board1.isGameOver:
            reward -= 50
            isDone = True
            self.timeAlive = 0
           

        return self.getState(False), reward, isDone


    def getSnakeVision(self):
        headX = self.board1.snake.body.deque[0].x
        headY = self.board1.snake.body.deque[0].y
        boardArray = self.board1.boardArray
        snakeDirection = self.board1.snake.currentDirection
        leftObstacle = 0
        rightObstacle = 0
        upObstacle = 0
        downObstacle = 0
        
        vision = np.full((9, 9),'1')
        rowIncr = -5

        #for i in range(9):
        #    rowIncr += 1
        #    columnIncr = -4
        #    for j in range(9):
        #        try:
        #            if headX + columnIncr >= 0 and headY + rowIncr >= 0:
        #                vision[i][j] = boardArray[int(headX + columnIncr)][int(headY + rowIncr)]
        #            else:
        #                vision[i][j] = "5"
        #        except:
        #            vision[i][j] = "5"
        #        columnIncr += 1
        try:
            if boardArray[int(headX - 1)][int(headY)] != "1":
                leftObstacle = 1
                
            else:
                leftObstacle = 0

            if boardArray[int(headX + 1)][int(headY)] != "1":
                rightObstacle = 1
                
            else:
                rightObstacle = 0

            if boardArray[int(headX)][int(headY - 1)] != "1":
                upObstacle = 1
                
            else:
                upObstacle = 0

            if boardArray[int(headX)][int(headY + 1)] != "1":
                downObstacle = 1
                
            else:
                downObstacle = 0

        except:
            pass
       
        return leftObstacle, rightObstacle, upObstacle, downObstacle