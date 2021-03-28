import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Game import Game
from Simulation import Simulation
from Graph import Graph
import time
from Color import Color

##GROS BOARD = 1300x800
##PETIT BOARD = 1000x700
##PAS DE PETIT BOARD POUR AI, JUSTE LE GROS /3

class Main:
    def __init__(self):
        self.showMainMenu()
        self.menuWindow = None
        self.running = True
        self.currentMenu = "MainMenu"
        self.snakeDAO = SnakeDAO()
        self.snakeDAO.dbConnection()
        self.currentGame = None
        self.currentSimulation = None
        self.graphWindow = None
        self.fpsClock = pygame.time.Clock()
        self.prevTime = time.time()
        self.deltaTime = 1.0
        self.color = Color()
        self.headColor = self.snakeDAO.getColors("head")
        self.bodyColor = self.snakeDAO.getColors("body")
        self.appleColor = self.snakeDAO.getColors("apple")

        print(self.headColor)

        if self.headColor == (0,0,0) or self.bodyColor == (0,0,0) or self.appleColor == (0,0,0):
            self.headColor = self.color.darkGreen
            self.bodyColor = self.color.lightGreen
            self.appleColor = self.color.red
            print(self.headColor)

            self.snakeDAO.saveColors(self.headColor,self.bodyColor,self.appleColor)
       

        
        #Window loop
        while self.running:
            self.fpsClock.tick(30)
            #now = time.time()
            #self.deltaTime = now - self.prevTime
            #self.prevTime = now

         

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.snakeDAO.dbCloseConnection()
                    self.running = False
            if self.currentMenu == "MainMenu":
                self.showMainMenu()
            elif self.currentMenu == "GameConfig":
                self.setGameConfig()
            elif self.currentMenu == "SimulationConfig":
                self.setSimulationConfig()
            elif self.currentMenu == "Game":
                self.currentGame.showGame()
            elif self.currentMenu == "Simulation":
                self.currentSimulation.showSimulation()
            elif self.currentMenu == "Graph":
                self.graphWindow.showGraphWindow()
            pygame.display.update()
                    

    def showMainMenu(self):

        buttonX = 650
        buttonY = 250
            
        (width, height) = (1500, 1000)
        self.menuWindow = pygame.display.set_mode((width,height))
        pygame.display.set_caption("S N A. I. K E")

        font = pygame.font.SysFont("arial", 60)
        text = font.render("S  N  A.  I.  K  E", 1, (0,255,0))

        self.menuWindow.blit(text, (585,75))
        

        gameButton = Button(75,225, buttonX, buttonY, (0,255,0), "Play")
        gameButton.drawButton(self.menuWindow)

        simulationButton = Button(75,225, buttonX, buttonY + 150, (0,255,0), "Simulation")
        simulationButton.drawButton(self.menuWindow)

        graphButton = Button(75,225, buttonX, buttonY + 300, (0,255,0), "Diagrams")
        graphButton.drawButton(self.menuWindow)

        quitButton = Button(75,225, buttonX, buttonY + 450, (0,255,0), "Quit")
        quitButton.drawButton(self.menuWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            if gameButton.clicked(mousePos):
                self.currentMenu = "GameConfig"
            elif simulationButton.clicked(mousePos):
                self.currentMenu = "SimulationConfig"
            elif graphButton.clicked(mousePos):
                self.graphWindow = Graph(self)
                self.currentMenu = "Graph"
            elif quitButton.clicked(mousePos):
                self.snakeDAO.dbCloseConnection()
                self.running = False

        #pygame.display.update()
        
        

    
    def setGameConfig(self):
        headColorButtons = [None] * 10
        bodyColorButtons = [None] * 10
        appleColorButtons = [None] * 10
        colors = self.color.getColors()
        i = 0
        j = 75

        self.menuWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        title = font.render("Configuration", 1, (0,255,0))
        self.menuWindow.blit(title, (625,75))

        font = pygame.font.SysFont("arial", 40)
        headColor = font.render("Head Color: ", 1, (0,255,0))
        self.menuWindow.blit(headColor, (250,175))

        for color in colors:
            headColorButtons[i] = Button(50, 50, 475 + j, 175, color, None)
            headColorButtons[i].drawButton(self.menuWindow)
            i += 1
            j += 75

        bodyColor = font.render("Body Color: ", 1, (0,255,0))
        self.menuWindow.blit(bodyColor, (250,300))

        i = 0
        j = 75
        for color in colors:
            bodyColorButtons[i] = Button(50, 50, 475 + j, 300, color, None)
            bodyColorButtons[i].drawButton(self.menuWindow)
            i += 1
            j += 75

        i = 0
        j = 75

        appleColor = font.render("Apple Color: ", 1, (0,255,0))
        self.menuWindow.blit(appleColor, (250,425))

        for color in colors:
            appleColorButtons[i] = Button(50, 50, 475 + j, 425, color, None)
            appleColorButtons[i].drawButton(self.menuWindow)
            i += 1
            j += 75

       
        startButton = Button(75,225, 500, 825, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 800, 825, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            for i in range(10):
                if headColorButtons[i].clicked(mousePos):
                    self.headColor = headColorButtons[i].color
                    
                if bodyColorButtons[i].clicked(mousePos):
                    self.bodyColor = bodyColorButtons[i].color

                if appleColorButtons[i].clicked(mousePos):
                    self.appleColor = appleColorButtons[i].color

            if startButton.clicked(mousePos):
                self.currentGame = Game(self, self.headColor, self.bodyColor, self.appleColor)
                self.snakeDAO.saveColors(self.headColor,self.bodyColor,self.appleColor)
                self.currentMenu = "Game"
            elif cancelButton.clicked(mousePos):
                self.currentMenu = "MainMenu"


        

        #pygame.display.update()

    
    def setSimulationConfig(self):

        self.menuWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        text = font.render("Configuration", 1, (0,255,0))

        self.menuWindow.blit(text, (625,75))
        
        startButton = Button(75,225, 500, 825, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 800, 825, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()
         
            if startButton.clicked(mousePos):
                self.currentSimulation = Simulation(self)
                self.currentMenu = "Simulation"
            elif cancelButton.clicked(mousePos):
                self.currentMenu = "MainMenu"


        #pygame.display.update()


if __name__ == "__main__":
    m = Main() 
