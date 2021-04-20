import pygame
import random
import numpy as np
from Snake import Snake
from Apple import Apple
import time

class Board:
    def __init__(self, game, height, width,leftPadding, topPadding, squareSize):
        self.game = game
        self.apple = None
        self.leftPadding = leftPadding - 18
        self.topPadding = topPadding - 18
        self.scaledWidth = width
        self.scaledHeight = height
        self.squareSize = squareSize
        self.snake = Snake(self.scaledHeight/2, self.scaledWidth/2)
        self.boardArray = np.full((self.scaledHeight, self.scaledWidth),'E')
        self.window = self.game.window
        self.isGameOver = False
        self.rowCount = self.boardArray.shape[0]
        self.columnCount = self.boardArray.shape[1]
        self.cumulTime = 0
        self.prevTime = time.time()
        self.updateBoardArray()
        self.addApple()
      
        

    def addApple(self):
        while True:
            x = random.randint(0, self.scaledHeight -1)
            y = random.randint(0, self.scaledWidth -1)
            if self.boardArray[x][y] == "1":
                self.apple = Apple(x,y)
                break
        

    def updateBoardArray(self):
        self.boardArray = np.full((self.scaledHeight, self.scaledWidth),'1')
        if not self.isGameOver:
            for i in self.snake.body.deque:
                if i.y < 60:
                    if i == self.snake.body.deque[0]:
                        self.boardArray[int(i.x), int(i.y)] = '2'
                    else:
                        self.boardArray[int(i.x),int(i.y)] = '3'
            
            if self.apple != None:
                self.boardArray[self.apple.x,self.apple.y] = '4'


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
        
        if self.snake.body.deque[0].x == -1 or self.snake.body.deque[0].y == -1:
            self.isGameOver = True
            




    def tic(self):
        try:
            
            now = time.time()
            deltaTime = now - self.prevTime
            self.prevTime = now
            self.cumulTime += deltaTime
            speed = 1/self.game.snakeSpeed


            posX = self.leftPadding
            squarePosition = self.squareSize + 2
            for i in range(0,self.rowCount):
                posX += squarePosition
                posY = self.topPadding
                for j in range(0,self.columnCount):
                    posY += squarePosition
                    
                    pygame.draw.rect(self.window, (18, 18, 18), (posX, posY, self.squareSize, self.squareSize), 0)

                    if self.boardArray[i][j] == "2":
                        pygame.draw.rect(self.window, self.game.headColor, (posX, posY, self.squareSize, self.squareSize), 0)
                        
                    elif self.boardArray[i][j] == "3":
                        pygame.draw.rect(self.window, self.game.bodyColor, (posX, posY, self.squareSize, self.squareSize), 0)

                    elif self.boardArray[i][j] == "4":
                            pygame.draw.rect(self.window, self.game.appleColor, (posX, posY, self.squareSize, self.squareSize), 0)

            #Gachette (faire le mouvement quand cumulTime devient plus grand que la vitesse, voir lignes 75 à6
            #  79)
            if self.cumulTime > speed:
                self.cumulTime -= speed
                #Action
                if self.snake.currentDirection != "paused":
                    self.snake.body.rotate(self.snake.snakeXMovement, self.snake.snakeYMovement)   

           

            self.snakeCollision()
            self.updateBoardArray()

        except IndexError:
            self.isGameOver = True
