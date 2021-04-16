import pygame
from Button import Button
from SnakeDAO import SnakeDAO
from Game import Game
from Simulation import Simulation
from Graph import Graph
import time
from Color import Color


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
        self.color = Color()
        self.headColor = self.snakeDAO.getColors("head")
        self.bodyColor = self.snakeDAO.getColors("body")
        self.appleColor = self.snakeDAO.getColors("apple")
        self.speed = 10
        self.boardSize = "small"
        self.numberOfEpisodes = 200


        if self.headColor == (0,0,0) or self.bodyColor == (0,0,0) or self.appleColor == (0,0,0):
            self.headColor = self.color.darkGreen
            self.bodyColor = self.color.lightGreen
            self.appleColor = self.color.red
           

            self.snakeDAO.saveColors(self.headColor,self.bodyColor,self.appleColor)
       

        
        #Window loop
        while self.running:
            self.fpsClock.tick(60)

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

        buttonX = 750
        buttonY = 350
            
        (width, height) = (1600, 1100)
        self.menuWindow = pygame.display.set_mode((width,height))
        pygame.display.set_caption("S N A. I. K E")

        font = pygame.font.SysFont("arial", 60)
        text = font.render("S  N  A.  I.  K  E", 1, (0,255,0))

        self.menuWindow.blit(text, (685,175))
        

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

        
        
        

    
    def setGameConfig(self):

        headColorButtons = [None] * 10
        bodyColorButtons = [None] * 10
        appleColorButtons = [None] * 10
        speedButtons = [None] * 3
        sizeButtons = [None] * 2
        colors = self.color.getColors()
        i = 0
        j = 75

        self.menuWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        title = font.render("Configuration", 1, (0,255,0))
        self.menuWindow.blit(title, (725,75))

        font = pygame.font.SysFont("arial", 40)
        headColor = font.render("Head Color: ", 1, (0,255,0))
        self.menuWindow.blit(headColor, (250,275))

        bodyColor = font.render("Body Color: ", 1, (0,255,0))
        self.menuWindow.blit(bodyColor, (250,400))

        appleColor = font.render("Apple Color: ", 1, (0,255,0))
        self.menuWindow.blit(appleColor, (250,525))

        for color in colors:
            headColorButtons[i] = Button(50, 50, 475 + j, 275, color, None)
            headColorButtons[i].drawButton(self.menuWindow)

            bodyColorButtons[i] = Button(50, 50, 475 + j, 400, color, None)
            bodyColorButtons[i].drawButton(self.menuWindow)

            appleColorButtons[i] = Button(50, 50, 475 + j, 525, color, None)
            appleColorButtons[i].drawButton(self.menuWindow)

            i += 1
            j += 75


        speed = font.render("Snake Speed: ", 1, (0,255,0))
        self.menuWindow.blit(speed, (250,650))

       
        j = 75
        for i in range(len(speedButtons)):
            speedButtons[i] = Button(75, 175, 475 + j, 650, (0,255,0), str(i+1))
            speedButtons[i].drawButton(self.menuWindow)
            j += 275

        size = font.render("Board Size: ", 1, (0,255,0))
        self.menuWindow.blit(size, (250,775))

        j = 75
        boardSize = "Small Board" 
        for i in range(2):
            sizeButtons[i] = Button(75, 325, 475 + j, 775, (0,255,0), boardSize)
            sizeButtons[i].drawButton(self.menuWindow)
            boardSize = "Large board"
            j += 400


        startButton = Button(75,225, 600, 975, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 900, 975, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            for i in range(len(colors)):
                if headColorButtons[i].clicked(mousePos):
                    self.headColor = headColorButtons[i].color
                    
                if bodyColorButtons[i].clicked(mousePos):
                    self.bodyColor = bodyColorButtons[i].color

                if appleColorButtons[i].clicked(mousePos):
                    self.appleColor = appleColorButtons[i].color

            for i in range(len(speedButtons)):
                if speedButtons[i].clicked(mousePos):
                    if speedButtons[i].text == "1":
                        self.speed = 10
                    elif speedButtons[i].text == "2":
                        self.speed = 15
                    else:
                        self.speed = 20
                  
                  

            for i in range(len(sizeButtons)):
                if sizeButtons[i].clicked(mousePos):
                    if sizeButtons[i].text == "Small Board":
                        self.boardSize = "small"
                    else:
                        self.boardSize = "large"
                    

            if startButton.clicked(mousePos):
                self.currentGame = Game(self, self.headColor, self.bodyColor, self.appleColor, self.speed, self.boardSize)
                self.snakeDAO.saveColors(self.headColor,self.bodyColor,self.appleColor)
                self.currentMenu = "Game"
            elif cancelButton.clicked(mousePos):
                self.currentMenu = "MainMenu"


    
    def setSimulationConfig(self):

        headColorButtons = [None] * 10
        bodyColorButtons = [None] * 10
        appleColorButtons = [None] * 10
        episodeButtons = [None] * 4
        sizeButtons = [None] * 2
        colors = self.color.getColors()
        i = 0
        j = 75

        self.menuWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        title = font.render("Configuration", 1, (0,255,0))
        self.menuWindow.blit(title, (725,75))

        font = pygame.font.SysFont("arial", 40)
        headColor = font.render("Head Color: ", 1, (0,255,0))
        self.menuWindow.blit(headColor, (250,275))

        bodyColor = font.render("Body Color: ", 1, (0,255,0))
        self.menuWindow.blit(bodyColor, (250,400))

        appleColor = font.render("Apple Color: ", 1, (0,255,0))
        self.menuWindow.blit(appleColor, (250,525))

        for color in colors:
            headColorButtons[i] = Button(50, 50, 475 + j, 275, color, None)
            headColorButtons[i].drawButton(self.menuWindow)

            bodyColorButtons[i] = Button(50, 50, 475 + j, 400, color, None)
            bodyColorButtons[i].drawButton(self.menuWindow)

            appleColorButtons[i] = Button(50, 50, 475 + j, 525, color, None)
            appleColorButtons[i].drawButton(self.menuWindow)

            i += 1
            j += 75

        episodes = font.render("Episode number: ", 1, (0,255,0))
        self.menuWindow.blit(episodes, (250,650))

        j = 75
        for i in range(len(episodeButtons)):
            episodeButtons[i] = Button(75, 125, 475 + j, 650, (0,255,0), str((i+1)*200))
            episodeButtons[i].drawButton(self.menuWindow)
            j += 200


        size = font.render("Board Size: ", 1, (0,255,0))
        self.menuWindow.blit(size, (250,775))

        j = 75
        boardSize = "Small Board" 
        for i in range(2):
            sizeButtons[i] = Button(75, 325, 475 + j, 775, (0,255,0), boardSize)
            sizeButtons[i].drawButton(self.menuWindow)
            boardSize = "Large board"
            j += 400


        startButton = Button(75,225, 600, 975, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 900, 975, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()

            for i in range(len(colors)):
                if headColorButtons[i].clicked(mousePos):
                    self.headColor = headColorButtons[i].color
                    
                if bodyColorButtons[i].clicked(mousePos):
                    self.bodyColor = bodyColorButtons[i].color

                if appleColorButtons[i].clicked(mousePos):
                    self.appleColor = appleColorButtons[i].color
                  
            
            for i in range(len(episodeButtons)):
                if episodeButtons[i].clicked(mousePos):
                    self.numberOfEpisodes = int(episodeButtons[i].text)
                    


            for i in range(len(sizeButtons)):
                if sizeButtons[i].clicked(mousePos):
                    if sizeButtons[i].text == "Small Board":
                        self.boardSize = "small"
                    else:
                        self.boardSize = "large"
                    

            if startButton.clicked(mousePos):
                self.currentSimulation = Simulation(self, self.headColor, self.bodyColor, self.appleColor, self.boardSize, self.numberOfEpisodes)
                self.snakeDAO.saveColors(self.headColor,self.bodyColor,self.appleColor)
                self.currentMenu = "Simulation"
            elif cancelButton.clicked(mousePos):
                self.currentMenu = "MainMenu"




if __name__ == "__main__":
    m = Main() 
