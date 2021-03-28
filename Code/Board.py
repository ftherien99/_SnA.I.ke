import pygame
import random
import numpy as np
from Snake import Snake
from Apple import Apple

class Board:
    def __init__(self, game):
        self.ticClock = pygame.time.Clock()
        self.apple = None
        self.width = 1200  
        self.height = 800 
        self.scaledWidth =  int(self.width/20)
        self.scaledHeight =  int(self.height/20)
        self.snake = Snake(1 * game.main.deltaTime, self.scaledWidth/2, self.scaledHeight/2)
        self.boardArray = np.full((self.scaledWidth, self.scaledHeight),'E')
        self.updateBoardArray()
        self.addApple()
        self.game = game
        self.gameWindow = self.game.gameWindow
        self.isGameOver = False
        self.rowCount = self.boardArray.shape[0]
        self.columnCount = self.boardArray.shape[1]
      
        

    def addApple(self):
        while True:
            x = random.randint(0, self.scaledWidth -1)
            y = random.randint(0, self.scaledHeight -1)
            if self.boardArray[x][y] == "E":
                self.apple = Apple(x,y)
                break

    def updateBoardArray(self):
        self.boardArray = np.full((self.scaledWidth, self.scaledHeight),'E')
        for i in self.snake.body.deque:
            if i.y < 60:
                if i == self.snake.body.deque[0]:
                    self.boardArray[int(i.x), int(i.y)] = 'H'
                else:
                    self.boardArray[int(i.x),int(i.y)] = 'B'
        
        if self.apple != None:
            self.boardArray[self.apple.x,self.apple.y] = 'A'


    def removeApple(self):
        self.apple = None

    def snakeCollision(self):
        if self.apple != None and self.snake.body.deque[0].x == self.apple.x and self.snake.body.deque[0].y == self.apple.y:
            self.removeApple()
            self.snake.body.grow(self.snake.currentDirection)
            self.addApple()
            self.game.score += 10

        for i in self.snake.body.deque:
            if i != self.snake.body.deque[0] and i.x == self.snake.body.deque[0].x and i.y == self.snake.body.deque[0].y:
                self.isGameOver = True




    def tic(self):
        try:
            posX = 92
            squareSize = 18

            for x in range(0,self.rowCount):
                posX += 20
                posY = 42
                for y in range(0,self.columnCount):
                    posY += 20
                    
                    #pygame.draw.rect(self.gameWindow, (0,0,255), (posX, posY, squareSize, squareSize), 0)
                    if self.boardArray[x][y] == "H":
                        pygame.draw.rect(self.gameWindow, self.game.headColor, (posX, posY, squareSize, squareSize), 0)
                        
                    elif self.boardArray[x][y] == "B":
                        pygame.draw.rect(self.gameWindow, self.game.bodyColor, (posX, posY, squareSize, squareSize), 0)

                    elif self.boardArray[x][y] == "A":
                            pygame.draw.rect(self.gameWindow, self.game.appleColor, (posX, posY, squareSize, squareSize), 0)
                

            if self.snake.currentDirection != "paused":
                self.snake.body.rotate(self.snake.snakeXMovement, self.snake.snakeYMovement)

            self.snakeCollision()
            self.updateBoardArray()

        except IndexError:
            self.isGameOver = True
