import time

import numpy as np
import pygame
import torch

from Agent import Agent
from Board import Board
from Button import Button


class Simulation:
    def __init__(self, main, headColor, bodyColor, appleColor, boardSize, numberOfEpisodes): 
        self.main = main
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.appleColor = appleColor
        self.snakeSpeed = 30
        self.boardSize = boardSize
        self.window = self.main.menuWindow
        self.simulaionSurface = None
        self.score = 0
        self.scoreCheck = 0
        self.board = None
        self.isNewHighscore = False
        self.isHighscoreSaved = False
        self.distance = None
        self.numberOfEpisodes = numberOfEpisodes
        self.startButton = None
        self.pauseButton = None
        self.quitButton = None
        self.agentCurrentScore = 0
        self.avgScore = 0
        self.episodes = 0
        self.steps = 0
        self.maxSteps = 10000
        self.timer = 0
        self.isPaused = False
        
        if self.boardSize == "small":
            self.boardWidth = 1005
            self.boardHeight = 605
            self.boardArrayX = 50
            self.boardArrayY = 30
            self.boardLeftPadding = 220
            self.boardTopPadding = 160
            self.qNetworkPath = "smallQNetwork.pth"
            

            self.displayedinfoX = 1245

            self.highScoreType = "small_board_ai"
            self.episodeType = "small_episodes"
        else:
            self.boardWidth = 1205
            self.boardHeight = 805
            self.boardArrayX = 60
            self.boardArrayY = 40
            self.boardLeftPadding = 100
            self.boardTopPadding = 60
            self.qNetworkPath = "largeQNetwork.pth"
            
            self.displayedinfoX = 1340

            self.highScoreType = "large_board_ai"
            self.episodeType = "large_episodes"

        self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)
        self.agent = Agent(12, 4, 0, self.qNetworkPath)

        if self.highscore == None:
            self.highscore = 0


        self.createBoard()
        self.showSimulation()
        
        

    def showSimulation(self):
        buttonX = 850
        buttonY = 1000

        self.window.fill((0,0,0))

        self.simulaionSurface = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding, self.boardTopPadding, self.boardWidth, self.boardHeight), 2)

        if self.score > self.highscore:    
            self.highscore = self.score
            self.isNewHighscore = True

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score: " + str(self.score), 1, (0,255,0))
        self.window.blit(scoreText, (100,1025))

        highscoreText = font.render("Highscore: " + str(self.highscore), 1, (0,255,0))
        self.window.blit(highscoreText, (375, 1025))

        agentRewardText = font.render("Cur. Reward: " + str(round(self.agentCurrentScore,2)), 1, (0,255,0))
        self.window.blit(agentRewardText, (self.displayedinfoX, 175))

        agentAvgRewardText = font.render("Avg. Reward: " + str(round(self.avgScore,2)), 1, (0,255,0))
        self.window.blit(agentAvgRewardText, (self.displayedinfoX, 250))

        episodeText = font.render("Episode:   " + str(self.episodes) + "/" + str(self.numberOfEpisodes), 1, (0,255,0))
        self.window.blit(episodeText, (self.displayedinfoX, 325))

        stepsText = font.render("Steps:   " + str(self.steps) + "/" + str(self.maxSteps), 1, (0,255,0))
        self.window.blit(stepsText, (self.displayedinfoX, 400))

        episodeTimeText = font.render("Episode time (sec): " + str(round(self.timer,0)), 1, (0,255,0))
        self.window.blit(episodeTimeText, (self.displayedinfoX, 475))


        self.startButton = Button(75, 225, buttonX, buttonY, (0,255,0), "Start")
        self.startButton.drawButton(self.window)

        if self.isPaused == False:
            self.pauseButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Pause")
        else:
            self.pauseButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Resume")

        self.pauseButton.drawButton(self.window)

        self.quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        self.quitButton.drawButton(self.window)


        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if self.startButton.clicked(mousePos):
                self.deepQLearning()

           
            elif self.quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"



       
    def deepQLearning(self): #R??F??RENCES: Test.py dans la section References/DQL exemple dans le git
        scoreWindow= []
        episodeCounter = 0

        for episode in range(self.numberOfEpisodes):
            start = time.time()
            self.score = 0
            self.scoreCheck = 0
            self.episodes = episode
            score = 0
            isDone = False
            self.board = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 18)
            state = self.getState()
            for steps in range(self.maxSteps):
                
                                
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        self.main.snakeDAO.dbCloseConnection()
                        self.main.running = False
                        exit()

                if pygame.mouse.get_pressed() == (1,0,0):
                    mousePos = pygame.mouse.get_pos()

                    if self.quitButton.clicked(mousePos):
                        self.main.currentMenu = "MainMenu"
                        break

                    elif self.pauseButton.clicked(mousePos):
                        if self.isPaused == False:
                            self.isPaused = True
                        else: 
                            self.isPaused = False

                if self.isPaused:
                    for i in range(1000000):
                        time.sleep(0.1)
                        for event in pygame.event.get(): 
                            if event.type == pygame.QUIT:
                                self.main.snakeDAO.dbCloseConnection()
                                self.main.running = False
                                exit()
                           
                        if pygame.mouse.get_pressed() == (1,0,0):
                            mousePos = pygame.mouse.get_pos()
                            if self.pauseButton.clicked(mousePos):
                                self.isPaused = False
                                time.sleep(0.5)
                                break
                
                action = self.agent.act(state)
                nextState, reward, isDone = self.simulationStep(action)
                self.agent.step(state, action, reward,nextState,isDone)
                state = nextState
                score += reward
                self.steps = steps
                self.agentCurrentScore = score
                self.board.tic()
                pygame.display.update()
                self.steps = steps
                self.showSimulation()
                end = time.time()
                self.timer = end - start
                if isDone:
                    self.main.snakeDAO.saveEpisode(self.episodeType, steps, self.timer, self.score, score)
                    break

            episodeCounter += 1
            scoreWindow.append(score)
            avgScore = np.mean(scoreWindow[-100:])
           
            self.avgScore = avgScore

            if self.isNewHighscore: 
                self.main.snakeDAO.saveHighscore(self.highScoreType,self.score)
                self.isNewHighscore = False
            
            self.score = 0

            if episodeCounter == 200:
                torch.save(self.agent.qNetworkLocal.state_dict(), self.qNetworkPath)
                print("Saving QNetwork")
                episodeCounter = 0
            
            if self.main.currentMenu == "MainMenu":
                break 

            

    def createBoard(self):
        self.board = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 18)
        


    def getState(self):

        left, right, up, down, topLeft, topRight, bottomLeft, bottomRight = self.getSnakeVision()

        state = []
        state.append(self.board.snake.body.deque[0].x)
        state.append(self.board.snake.body.deque[0].y)
        state.append(self.board.apple.x)
        state.append(self.board.apple.y)
        state.append(left)
        state.append(right)
        state.append(up)
        state.append(down)
        state.append(topLeft)
        state.append(topRight)
        state.append(bottomLeft)
        state.append(bottomRight)


        state = np.array(state)

        return state

    def simulationStep(self, action):
        reward = 0
        isDone = False
       
        appleX = self.board.apple.x
        appleY = self.board.apple.y

        headX = self.board.snake.body.deque[0].x
        headY = self.board.snake.body.deque[0].y

        temp = 0

        if self.distance == None:
            self.distance =  ((((headX - appleX)**2) + ((headY - appleY)**2))**0.5)
            
        else:
            temp = ((((headX - appleX)**2) + ((headY - appleY)**2))**0.5)


        if action == 0:
            self.board.snake.snakeController.changeDirection("up")
        elif action == 1:
            self.board.snake.snakeController.changeDirection("down")
        elif action == 2:
            self.board.snake.snakeController.changeDirection("left")
        elif action == 3:
            self.board.snake.snakeController.changeDirection("right")

       
        if temp < self.distance:
            reward += 0.5
            self.distance = temp
        else:
            reward -= 0.1
            self.distance = temp

        if self.scoreCheck < self.score:
            reward += 30
            self.scoreCheck = self.score

        if self.board.isGameOver:
            reward -= 50
            isDone = True
            self.timeAlive = 0
           

        return self.getState(), reward, isDone


    def getSnakeVision(self):
        headX = self.board.snake.body.deque[0].x
        headY = self.board.snake.body.deque[0].y
        boardArray = self.board.boardArray
        boardArrayX = self.boardArrayX - 1
        boardArrayY = self.boardArrayY - 1
        leftObstacle = 0
        rightObstacle = 0
        upObstacle = 0
        downObstacle = 0
        topLeftObstacle = 0
        topRightObstacle = 0
        bottomLeftObstacle = 0
        bottomRightObstacle = 0

        try:
            i = 1
            while True:
                if boardArray[int(headX - i)][int(headY)] != "1" and boardArray[int(headX - i)][int(headY)] != "4" or int(headX - i) < 0:
                    if headX == 0:
                        leftObstacle = 1
                        break
                    else:
                        leftObstacle = i
                        break    
                else:
                    i += 1

            i = 1
            while True:
                try:      
                    if boardArray[int(headX + i)][int(headY)] != "1" and boardArray[int(headX + i)][int(headY)] != "4":
                        rightObstacle = i
                        break
                    elif int(headX + i) == boardArrayX:
                        rightObstacle = i + 1
                        break
                    else:
                        i += 1
                except:
                    rightObstacle = 1
                    break

            i = 1
            while True:
                try:      
                    if boardArray[int(headX)][int(headY + i)] != "1" and boardArray[int(headX)][int(headY + i)] != "4":
                        downObstacle = i
                        break
                    elif int(headY + i) == boardArrayY:
                        downObstacle = i + 1
                        break
                    else:
                        i += 1
                except:
                    downObstacle = 1
                    break


            i = 1
            while True:
                if boardArray[int(headX)][int(headY - i)] != "1" and boardArray[int(headX)][int(headY - i)] != "4" or int(headY - i) < 0:
                    if headY == 0:
                        upObstacle = 1
                        break
                    else:
                        upObstacle = i
                        break    
                else:
                    i += 1

            i = 1
            while True:

                if boardArray[int(headX - i)][int(headY - i)] != "1" and boardArray[int(headX - i)][int(headY -i)] != "4" or int(headX - i) < 0 or int(headY - i) < 0:
                    if headY == 0:
                        topLeftObstacle = 1
                        break
                    elif headX == 0:
                        topLeftObstacle = 1
                        break
                    else:
                        topLeftObstacle = i
                        break
                else:
                    i += 1

            i = 1
            while True:
                try:      
                    if boardArray[int(headX + i)][int(headY - i)] != "1" and boardArray[int(headX + i)][int(headY - i)] != "4":
                        topRightObstacle = i
                        break
                    elif int(headX + i) == boardArrayX:
                        topRightObstacle = i + 1
                        break
                    elif int(headY - i) < 0:
                        topRightObstacle = i
                        break
                    else:
                        i += 1
                except:
                    topRightObstacle = 1
                    break

            i = 1
            while True:
                try:      
                    if boardArray[int(headX - i)][int(headY + i)] != "1" and boardArray[int(headX - i)][int(headY + i)] != "4":
                        bottomLeftObstacle = i
                        break
                    elif int(headY + i) == boardArrayY:
                        bottomLeftObstacle = i + 1
                        break
                    elif int(headX - i) < 0:
                        bottomLeftObstacle = i
                        break
                    else:
                        i += 1
                except:
                    bottomLeftObstacle = 1
                    break

            i = 1
            while True:
                try:      
                    if boardArray[int(headX + i)][int(headY + i)] != "1" and boardArray[int(headX + i)][int(headY + i)] != "4":
                        bottomRightObstacle = i
                        break
                    elif int(headY + i) == boardArrayY:
                        bottomRightObstacle = i + 1
                        break
                    elif int(headX + i) == boardArrayX:
                        bottomRightObstacle = i + 1
                        break
                    else:
                        i += 1
                except:
                    bottomRightObstacle = 1
                    break
        except:
            pass
        
        return leftObstacle, rightObstacle, upObstacle, downObstacle, topLeftObstacle, topRightObstacle, bottomLeftObstacle, bottomRightObstacle
