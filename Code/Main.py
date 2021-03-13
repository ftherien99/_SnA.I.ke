import pygame
from Button import Button
from SnakeDAO import SnakeDAO

class Main:
    def __init__(self):
        self.showMainMenu()
        self.menuWindow = None
        self.running = True
        self.currentMenu = "MainMenu"
        self.showMainMenu()
        self.setGameConfig()
        self.setSimulationConfig()
        self.snakeDAO = SnakeDAO()
        self.snakeDAO.dbConnection()
        
        #Window loop
        while self.running:

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
                    

    def showMainMenu(self):

        buttonX = 395
        buttonY = 200
            
        (width, height) = (1000, 800)
        self.menuWindow = pygame.display.set_mode((width,height))
        pygame.display.set_caption("S N A. I. K E")

        font = pygame.font.SysFont("arial", 60)
        text = font.render("S  N  A.  I.  K  E", 1, (0,255,0))

        self.menuWindow.blit(text, (335,75))
        

        gameButton = Button(75,225, buttonX, buttonY, (0,255,0), "Play")
        gameButton.drawButton(self.menuWindow)

        simulationButton = Button(75,225, buttonX, buttonY + 150, (0,255,0), "Simulation")
        simulationButton.drawButton(self.menuWindow)

        graphButton = Button(75,225, buttonX, buttonY + 300, (0,255,0), "Diagrams")
        graphButton.drawButton(self.menuWindow)

        quitButton = Button(75,225, buttonX, buttonY + 450, (0,255,0), "Quit")
        quitButton.drawButton(self.menuWindow)

        pygame.display.update()
        
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                mousePos = pygame.mouse.get_pos()

                if gameButton.clicked(mousePos):
                    self.currentMenu = "GameConfig"
                elif simulationButton.clicked(mousePos):
                    self.currentMenu = "SimulationConfig"
                elif graphButton.clicked(mousePos):
                    pass
                elif quitButton.clicked(mousePos):
                    self.snakeDAO.dbCloseConnection()
                    self.running = False

            elif event.type == pygame.QUIT:
                    self.snakeDAO.dbCloseConnection()
                    self.running = False

    
    def setGameConfig(self):

        self.menuWindow.fill((0,0,0))
        
        startButton = Button(75,225, 250, 675, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 550, 675, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                if startButton.clicked(mousePos):
                    pass
                elif cancelButton.clicked(mousePos):
                    self.currentMenu = "MainMenu"

            elif event.type == pygame.QUIT:
                    self.running = False

        pygame.display.update()

    
    def setSimulationConfig(self):

        self.menuWindow.fill((0,0,0))
        

        startButton = Button(75,225, 250, 675, (0,255,0), "Start Game")
        startButton.drawButton(self.menuWindow)

        cancelButton = Button(75,225, 550, 675, (255,0,0), "Cancel")
        cancelButton.drawButton(self.menuWindow)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                if startButton.clicked(mousePos):
                    pass
                elif cancelButton.clicked(mousePos):
                    self.currentMenu = "MainMenu"

            elif event.type == pygame.QUIT:
                    self.running = False

        pygame.display.update()

        


    


if __name__ == "__main__":
    m = Main() 
