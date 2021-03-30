import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board

class Simulation:
    def __init__(self, main, headColor, bodyColor, appleColor, boardSize): 
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.appleColor = appleColor
        self.snakeSeed = 1
        self.boardSize = boardSize
        self.window = self.main.menuWindow
        self.gameSurface = None
        self.score = 0
        self.board1 = None
        self.board2 = None
        self.board3 = None
        self.board4 = None
        self.isNewHighscore = False
        self.isHighscoreSaved = False

        if self.boardSize == "small":
            self.boardWidth = 1005/2
            self.boardHeight = 605/2
            self.boardArrayX = 50
            self.boardArrayY = 30
            self.boardLeftPadding = 110
            self.boardTopPadding = 85
            self.highScoreType = "small_board_ai"
        else:
            self.boardWidth = 1205/3
            self.boardHeight = 805/3
            self.boardArrayX = 60
            self.boardArrayY = 40
            self.boardLeftPadding = 210
            self.boardTopPadding = 160
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

        gameBoard1 = pygame.draw.rect(self.window, (0,255,0), (100, 75, self.boardWidth, self.boardHeight), 2)
        gameBoard2 = pygame.draw.rect(self.window, (0,255,0), (650, 75, self.boardWidth, self.boardHeight), 2)
        gameBoard3 = pygame.draw.rect(self.window, (0,255,0), (100, 425, self.boardWidth, self.boardHeight), 2)
        gameBoard4 = pygame.draw.rect(self.window, (0,255,0), (650, 425, self.boardWidth, self.boardHeight), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score: " + str(self.score), 1, (0,255,0))
        self.window.blit(scoreText, (100,1025))

        highscoreText = font.render("Highscore: " + str(self.highscore), 1, (0,255,0)) #va aller chercher la valeur dans la bd
        self.window.blit(highscoreText, (375,1025))

        agentRewardText = font.render("Agent Reward:", 1, (0,255,0))
        self.window.blit(agentRewardText, (1275,250))

        episodeText = font.render("Episode:", 1, (0,255,0))
        self.window.blit(episodeText, (1275,325))

        stepsText = font.render("Steps:", 1, (0,255,0))
        self.window.blit(stepsText, (1275,400))

        episodeTimeText = font.render("Episode time (sec):", 1, (0,255,0))
        self.window.blit(episodeTimeText, (1275,475))

        pauseButton = Button(75,225, buttonX, buttonY, (0,255,0), "Pause")
        pauseButton.drawButton(self.window)

        resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        resetButton.drawButton(self.window)

        quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        quitButton.drawButton(self.window)

       
        self.board1.tic()
        self.board2.tic()
        self.board3.tic()
        self.board4.tic()

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if pauseButton.clicked(mousePos):
                self.board.snake.snakeController.changeDirection("paused")
            elif resetButton.clicked(mousePos):
                self.createBoards()
                self.score = 0
                self.highscore = self.main.snakeDAO.getHighscore(self.highScoreType)
                self.isNewHighscore = False
            elif quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"

       


    def createBoards(self):
        self.board1 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding, 8)
        self.board2 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + 550, self.boardTopPadding, 8)
        self.board3 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding, self.boardTopPadding + 350, 8)
        self.board4 = Board(self,self.boardArrayX, self.boardArrayY, self.boardLeftPadding + 550, self.boardTopPadding + 350, 8)
