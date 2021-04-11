import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board
from Agent import Agent
from collections import deque
import numpy as np
import torch

class Simulation:
    def __init__(self, main, headColor, bodyColor, appleColor, boardSize): 
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.appleColor = appleColor
        self.snakeSpeed = 70
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
        self.agent = Agent(4, 4, 0)
        

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

        pauseButton = Button(75,225, buttonX, buttonY, (0,255,0), "Pause")
        pauseButton.drawButton(self.window)

        resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        resetButton.drawButton(self.window)

        quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        quitButton.drawButton(self.window)

        self.board2.tic()
        self.board3.tic()
        self.board4.tic()


        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if pauseButton.clicked(mousePos):
               #self.board1.snake.snakeController.changeDirection("paused")
               #self.board2.snake.snakeController.changeDirection("paused")
               #self.board3.snake.snakeController.changeDirection("paused")
               #self.board4.snake.snakeController.changeDirection("paused")
               self.deepQLearning()
            elif resetButton.clicked(mousePos):
                self.createBoards()
                self.score = 0
                self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)
                self.isNewHighscore = False
            elif quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"

       
    def deepQLearning(self):
        scoreWindow, eps = [], []
        epsilon = 1.0
        epsilonMin = 0.01
        epsilonDecr = 0.995
       

        for episode in range(7500):
            score = 0
            isDone = False
            self.board1 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 8)
            state = self.getState()
            while not isDone:
                pygame.event.get()
                action = self.agent.act(state)
                nextState, reward, isDone = self.simulationStep(action)
                self.agent.step(state, action, reward,nextState,isDone)
                state = nextState
                score += reward
                self.board1.tic()
                pygame.display.update()
                if isDone:
                    torch.save(self.agent.qNetworkLocal.state_dict(), 'checkpoint.pth')
                    break
            scoreWindow.append(score)
            eps.append(epsilon)
            avgScore = np.mean(scoreWindow[-100:])
            print("episode: ", episode, "  score %.2f " % score, "  average score %.2f:" % avgScore, "  epsilon %.2f" % epsilon)
            epsilon = max(epsilonMin, epsilonDecr * epsilon)
            

        


    def createBoards(self):
        self.board1 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 8)
        self.board2 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + self.boardDistanceX + 10, self.boardTopPadding, 8)
        self.board3 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding + self.boardDistanceY + 10, 8)
        self.board4 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + self.boardDistanceX + 10, self.boardTopPadding + self.boardDistanceY + 10, 8)


    def getState(self):
        state = np.zeros(4)
        state[0] = self.board1.snake.body.deque[0].x
        state[1] = self.board1.snake.body.deque[0].y
        state[2] = self.board1.snake.body.length
        state[3] = 0

        return state

    def simulationStep(self, action):
        reward = 0
        isDone = False

        if action == 0:
            self.board1.snake.snakeController.changeDirection("up")
        elif action == 1:
            self.board1.snake.snakeController.changeDirection("down")
        elif action == 2:
            self.board1.snake.snakeController.changeDirection("left")
        elif action == 3:
            self.board1.snake.snakeController.changeDirection("right")


        if self.board1.isGameOver == False:
            reward += 0.5

        #if self.board1.snake.body.deque[0].x == self.board1.apple.x:
        #    reward += 50
        #    print("X")
#
        #if self.board1.snake.body.deque[0].y == self.board1.apple.y:
        #    reward += 50
        #    print("Y")
#
        #if self.scoreCheck < self.score:
        #    self.scoreCheck += 10
        #    reward += 300
        #    print("APPLE")

        if self.board1.isGameOver:
            reward -= 200
            isDone = True
           

        return self.getState(), reward, isDone