import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board


class Game:
    def __init__(self, main): #headColor, bodyColor, appleColor, speed, boardSize
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.gameWindow = self.main.menuWindow
        self.gameSurface = None
        self.score = 0
        self.highscore = self.main.snakeDAO.getHighscore("large_board_play")
        self.board = None
        self.createBoard()
        self.showGame()
        self.isNewHighscore = False
       
        
    def showGame(self):
        
        buttonX = 750
        buttonY = 900

        self.gameWindow.fill((0,0,0))

        pygame.display.set_caption("S N A. I. K E")

        self.gameSurface = pygame.draw.rect(self.gameWindow, (0,255,0), (110, 60, 1200, 800), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score: " + str(self.score), 1, (0,255,0))
        self.gameWindow.blit(scoreText, (100,925))

        highscoreText = font.render("Highscore: " + str(self.highscore), 1, (0,255,0)) #va aller chercher la valeur dans la bd
        self.gameWindow.blit(highscoreText, (375,925))

        if self.score > self.highscore:
            self.highscore = self.score
            self.isNewHighscore = True


        pauseButton = Button(75,225, buttonX, buttonY, (0,255,0), "Pause")
        pauseButton.drawButton(self.gameWindow)

        resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        resetButton.drawButton(self.gameWindow)

        quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        quitButton.drawButton(self.gameWindow)
        
        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if pauseButton.clicked(mousePos):
                self.board.snake.snakeController.changeDirection("paused")
            elif resetButton.clicked(mousePos):
                self.createBoard()
                self.score = 0
                self.highscore = self.main.snakeDAO.getHighscore("large_board_play")
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

        else:
            font = pygame.font.SysFont("arial", 60)
            text = font.render("GAME OVER", 1, (255,0,0))
            self.gameWindow.blit(text, (585,75))

            scoreText = font.render("Final Score: " + str(self.score), 1, (0,255,0))
            self.gameWindow.blit(scoreText, (585,300))

            if self.isNewHighscore:
                scoreText = font.render("New Highscore!", 1, (0,255,0))
                self.gameWindow.blit(scoreText, (570,450))
                self.main.snakeDAO.saveHighscore("large_board_play",self.score)



        #pygame.display.update()
        self.fpsClock.tick(60)
      
        

    def createBoard(self):
        self.board = Board(self)
