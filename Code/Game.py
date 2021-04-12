import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board
import time
import numpy as np


class Game:
    def __init__(self, main, headColor, bodyColor, appleColor, snakeSpeed, boardSize): #speed, boardSize
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.appleColor = appleColor
        self.snakeSpeed = snakeSpeed
        self.boardSize = boardSize
        self.window = self.main.menuWindow
        self.gameSurface = None
        self.score = 0
        self.board = None
        self.isNewHighscore = False
        self.isHighscoreSaved = False

        if self.boardSize == "small":
            self.boardWidth = 1005
            self.boardHeight = 605
            self.boardArrayX = 50
            self.boardArrayY = 30
            self.boardLeftPadding = 320
            self.boardTopPadding =160
            self.highScoreType = "small_board_play"
        else:
            self.boardWidth = 1205
            self.boardHeight = 805
            self.boardArrayX = 60
            self.boardArrayY = 40
            self.boardLeftPadding = 210
            self.boardTopPadding = 60
            self.highScoreType = "large_board_play"

        self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)

        if self.highscore == None:
            self.highscore = 0

        self.createBoard()
        self.showGame()
       
        
    def showGame(self):
        
        buttonX = 850
        buttonY = 1000

        self.window.fill((0,0,0))

        pygame.display.set_caption("S N A. I. K E")

        self.gameSurface = pygame.draw.rect(self.window, (0,255,0), (self.boardLeftPadding, self.boardTopPadding, self.boardWidth, self.boardHeight), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score: " + str(self.score), 1, (0,255,0))
        self.window.blit(scoreText, (100,1025))

        highscoreText = font.render("Highscore: " + str(self.highscore), 1, (0,255,0))
        self.window.blit(highscoreText, (375,1025))

        if self.score > self.highscore:
            self.highscore = self.score
            self.isNewHighscore = True


        pauseButton = Button(75,225, buttonX, buttonY, (0,255,0), "Pause")
        pauseButton.drawButton(self.window)

        resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        resetButton.drawButton(self.window)

        quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        quitButton.drawButton(self.window)
        
        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if pauseButton.clicked(mousePos):
                self.board.snake.snakeController.changeDirection("paused")
            elif resetButton.clicked(mousePos):
                self.createBoard()
                self.score = 0
                self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)
                self.isNewHighscore = False
            elif quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"

        elif pygame.key.get_pressed()[pygame.K_w]:
            self.board.snake.snakeController.changeDirection("up")
        
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.board.snake.snakeController.changeDirection("down")

        elif pygame.key.get_pressed()[pygame.K_a]:
            self.board.snake.snakeController.changeDirection("left")

        elif pygame.key.get_pressed()[pygame.K_d]:
            self.board.snake.snakeController.changeDirection("right")

     
        if self.board.isGameOver == False:
            self.board.tic()
            self.getSnakeVision()
 

        else:
            font = pygame.font.SysFont("arial", 60)
            text = font.render("GAME OVER", 1, (255,0,0))
            self.window.blit(text, (685,175))

            scoreText = font.render("Final Score: " + str(self.score), 1, (0,255,0))
            self.window.blit(scoreText, (685,400))

            if self.isNewHighscore:
                scoreText = font.render("New Highscore!", 1, (0,255,0))
                self.window.blit(scoreText, (670,550))
                if self.isHighscoreSaved != True:
                    self.main.snakeDAO.saveHighscore(self.highScoreType,self.score)
                    self.isHighscoreSaved = True

      
        

    def createBoard(self):
        self.board = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 18)
