import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Board import Board


class Game:
    def __init__(self, main): #headColor, bodyColor, appleColor, speed, boardSize
        self.snakeDAO = SnakeDAO()
        self.fpsClock = pygame.time.Clock()
        self.main = main
        self.gameWindow = self.main.menuWindow
        self.gameSurface = None
        self.isBoardInitialized = False
        self.board = None
        self.createBoard()
        self.showGame()
       
        
    def showGame(self):
        buttonX = 750
        buttonY = 900

        self.gameWindow.fill((0,0,0))

        pygame.display.set_caption("S N A. I. K E")

        self.gameSurface = pygame.draw.rect(self.gameWindow, (0,255,0), (100, 60, 1300, 800), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score:", 1, (0,255,0))
        self.gameWindow.blit(scoreText, (100,925))

        score = font.render("0", 1, (0,255,0))
        self.gameWindow.blit(score, (180,925))

        highscoreText = font.render("Highscore:", 1, (0,255,0)) #va aller chercher la valeur dans la bd
        self.gameWindow.blit(highscoreText, (375,925))


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
                pass
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

        
        if self.isBoardInitialized:
            self.board.tic()
            
           

        pygame.display.update()
        self.fpsClock.tick(10)
        
        

        

    def createBoard(self):
        self.board = Board(self)
        self.isBoardInitialized = True
