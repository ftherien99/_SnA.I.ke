import pygame
from Button import Button
from SnakeDAO import SnakeDAO

class Simulation:
    def __init__(self, main): #headColor, bodyColor, appleColor, speed, boardSize
        self.snakeDAO = SnakeDAO()
        self.main = main
        self.simulationWindow = self.main.menuWindow
        self.showSimulation()
        


    def showSimulation(self):
        buttonX = 750
        buttonY = 900

        self.simulationWindow.fill((0,0,0))

        gameBoard1 = pygame.draw.rect(self.simulationWindow, (0,255,0), (100, 75, 1300/3, 800/3), 2)
        gameBoard2 = pygame.draw.rect(self.simulationWindow, (0,255,0), (600, 75, 1300/3, 800/3), 2)
        gameBoard3 = pygame.draw.rect(self.simulationWindow, (0,255,0), (100, 425, 1300/3, 800/3), 2)
        gameBoard4 = pygame.draw.rect(self.simulationWindow, (0,255,0), (600, 425, 1300/3, 800/3), 2)

        font = pygame.font.SysFont("arial", 28)
        scoreText = font.render("Score:", 1, (0,255,0))
        self.simulationWindow.blit(scoreText, (100,925))

        score = font.render("0", 1, (0,255,0))
        self.simulationWindow.blit(score, (180,925))

        highscoreText = font.render("Highscore:", 1, (0,255,0)) #va aller chercher la valeur dans la bd
        self.simulationWindow.blit(highscoreText, (375,925))

        agentRewardText = font.render("Agent Reward:", 1, (0,255,0))
        self.simulationWindow.blit(agentRewardText, (1100,250))

        episodeText = font.render("Episode:", 1, (0,255,0))
        self.simulationWindow.blit(episodeText, (1100,325))

        stepsText = font.render("Steps:", 1, (0,255,0))
        self.simulationWindow.blit(stepsText, (1100,400))

        episodeTimeText = font.render("Episode time (sec):", 1, (0,255,0))
        self.simulationWindow.blit(episodeTimeText, (1100,475))

        pauseButton = Button(75,225, buttonX, buttonY, (0,255,0), "Pause")
        pauseButton.drawButton(self.simulationWindow)

        resetButton = Button(75,225, buttonX + 250, buttonY, (0,255,0), "Reset")
        resetButton.drawButton(self.simulationWindow)

        quitButton = Button(75,225, buttonX + 500, buttonY, (255,0,0), "Quit")
        quitButton.drawButton(self.simulationWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if pauseButton.clicked(mousePos):
                self.board1.snake.snakeController.changeDirection("paused")
                self.board2.snake.snakeController.changeDirection("paused")
                self.board3.snake.snakeController.changeDirection("paused")
                self.board4.snake.snakeController.changeDirection("paused")
            elif resetButton.clicked(mousePos):
                pass
            elif quitButton.clicked(mousePos):
                self.main.currentMenu = "MainMenu"

        pygame.display.update()