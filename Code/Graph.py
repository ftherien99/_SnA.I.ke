import pygame
from Button import Button
from SnakeDAO import SnakeDAO

class Graph:
    def __init__(self, main):
        self.main = main
        self.snakeDAO = SnakeDAO()
        self.graphWindow = self.main.menuWindow
        self.showGraphWindow()

    def showGraphWindow(self):

        buttonX = 215
        buttonY = 175
        
        self.graphWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        text = font.render("Graphs", 1, (0,255,0))
        self.graphWindow.blit(text, (700,75))
        
        episodePointButton = Button(75,225, buttonX, buttonY, (0,255,0), "Points/Episode")
        episodePointButton.drawButton(self.graphWindow)

        episodeRewardButton = Button(75,225, buttonX + 300, buttonY, (0,255,0), "Reward/Episode")
        episodeRewardButton.drawButton(self.graphWindow)

        episodeTimeButton = Button(75,225, buttonX + 600, buttonY, (0,255,0), "Time/Episode")
        episodeTimeButton.drawButton(self.graphWindow)

        episodeStepsButton = Button(75,225, buttonX + 900, buttonY, (0,255,0), "Steps/Episode")
        episodeStepsButton.drawButton(self.graphWindow)

        text = font.render("Board size", 1, (0,255,0))
        self.graphWindow.blit(text, (665,350))

        smallButton = Button(75,225, buttonX + 300, 450, (0,255,0), "Small")
        smallButton.drawButton(self.graphWindow)

        largeButton = Button(75,225, buttonX + 600, 450, (0,255,0), "Large")
        largeButton.drawButton(self.graphWindow)

        text = font.render("Confirm", 1, (0,255,0))
        self.graphWindow.blit(text, (695,600))

        showButton = Button(75,225, 670, 700, (0,255,0), "Show Graph")
        showButton.drawButton(self.graphWindow)

        quitButton = Button(75,225, 50, 900, (255,0,0), "Main Menu")
        quitButton.drawButton(self.graphWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()
         
            if quitButton.clicked(mousePos): 
                self.main.currentMenu = "MainMenu"
            
