import pygame
from Button import Button
from bokeh.plotting import figure,output_file, show

class Graph:
    def __init__(self, main):
        self.main = main
        self.graphWindow = self.main.menuWindow
        self.showGraphWindow()
        self.currentGraph = "episodeScore"
        self.boardSize = "small_episodes"

    def showGraphWindow(self):

        buttonX = 265
        buttonY = 175
        
        self.graphWindow.fill((0,0,0))

        font = pygame.font.SysFont("arial", 60)
        text = font.render("Graphs", 1, (0,255,0))
        self.graphWindow.blit(text, (750,75))
        
        episodeScoreButton = Button(75,225, buttonX, buttonY, (0,255,0), "Points/Episode")
        episodeScoreButton.drawButton(self.graphWindow)

        episodeRewardButton = Button(75,225, buttonX + 300, buttonY, (0,255,0), "Reward/Episode")
        episodeRewardButton.drawButton(self.graphWindow)

        episodeTimeButton = Button(75,225, buttonX + 600, buttonY, (0,255,0), "Time/Episode")
        episodeTimeButton.drawButton(self.graphWindow)

        episodeStepsButton = Button(75,225, buttonX + 900, buttonY, (0,255,0), "Steps/Episode")
        episodeStepsButton.drawButton(self.graphWindow)

        text = font.render("Board size", 1, (0,255,0))
        self.graphWindow.blit(text, (715,350))

        smallButton = Button(75,225, buttonX + 300, 450, (0,255,0), "Small")
        smallButton.drawButton(self.graphWindow)

        largeButton = Button(75,225, buttonX + 600, 450, (0,255,0), "Large")
        largeButton.drawButton(self.graphWindow)

        text = font.render("Confirm", 1, (0,255,0))
        self.graphWindow.blit(text, (735,600))

        showButton = Button(75,225, buttonX + 440, 700, (0,255,0), "Show Graph")
        showButton.drawButton(self.graphWindow)

        quitButton = Button(75,225, 50, 900, (255,0,0), "Main Menu")
        quitButton.drawButton(self.graphWindow)

        if pygame.mouse.get_pressed() == (1,0,0):
            mousePos = pygame.mouse.get_pos()
         
            if quitButton.clicked(mousePos): 
                self.main.currentMenu = "MainMenu"
            
            elif episodeScoreButton.clicked(mousePos):
                self.currentGraph = "episodeScore"
            elif episodeRewardButton.clicked(mousePos):
                self.currentGraph = "episodeReward"
            elif episodeStepsButton.clicked(mousePos):
                self.currentGraph = "episodeStep"
            elif episodeTimeButton.clicked(mousePos):
                self.currentGraph = "episodeTime"

            elif smallButton.clicked(mousePos):
                self.boardSize = "small_episodes"
            elif largeButton.clicked(mousePos):
                self.boardSize = "large_episodes"


            elif showButton.clicked(mousePos):
                if self.currentGraph == "episodeScore":
                    self.graphBuilder("Scores", "Scores/Episodes", "Score by episodes", self.main.snakeDAO.getEpisodes(self.boardSize), self.main.snakeDAO.getEpisodeScore(self.boardSize))
                elif self.currentGraph == "episodeReward":
                    self.graphBuilder("Rewards", "Rewards/Episodes", "Rewards by epsiodes", self.main.snakeDAO.getEpisodes(self.boardSize), self.main.snakeDAO.getEpisodeReward(self.boardSize))
                elif self.currentGraph == "episodeStep":
                    self.graphBuilder("Steps", "Steps/Episodes", "Steps by episodes", self.main.snakeDAO.getEpisodes(self.boardSize), self.main.snakeDAO.getEpisodeSteps(self.boardSize))
                elif self.currentGraph == "episodeTime":
                    self.graphBuilder("Time(sec)", "Time(sec)/Episodes", "Time(sec) by episodes", self.main.snakeDAO.getEpisodes(self.boardSize), self.main.snakeDAO.getEpisodeTime(self.boardSize))

    
    def graphBuilder(self, yLabel, graphTitle, legend, xValues, yValues):  #reference: https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html
        output_file("snaikeGraph.html")

        plot = figure(title = graphTitle, x_axis_label = "Episodes", y_axis_label = yLabel, plot_width = 1500, plot_height=1500)
        plot.line(xValues, yValues, legend_label = legend, line_width = 1)
        plot.circle(xValues, yValues, size = 8)
        show(plot)