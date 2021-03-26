import pygame
import numpy as np
from Snake import Snake
from Apple import Apple

class Board:
    def __init__(self, game):
        self.ticClock = pygame.time.Clock()
        self.apple = 3
        self.width = 1300  
        self.height = 800 
        self.scaledWidth = self.width//20
        self.scaledHeight = self.height//20
        self.snake = Snake(20, self.width/2, self.height/2)
        #self.boardArray = np.full((650, 400),'E')
        self.game = game
        self.gameWindow = game.gameWindow
        self.isGameOver = False

       #for i in range(self.snake.body.length):
       #    if i == 0:
       #        self.boardArray[self.width//2, self.height//2] = 'H'
       #        pygame.draw
       #    else:
       #        self.boardArray[self.width//2 + 1, self.height//2] = 'B'

        
      
        

    def addApple(self):
        x = 710
        y = 600
        self.apple = Apple(x,y)

    def removeApple(self):
        self.apple = None

    def snakeCollision(self):
        if self.apple != None and self.snake.body.deque[0].x == self.apple.x and self.snake.body.deque[0].y == self.apple.y:
            self.removeApple()

    def tic(self):
        if self.snake.currentDirection != "paused":
            self.snake.body.rotate(self.snake.snakeXMovement,self.snake.snakeYMovement)
        for i in self.snake.body.deque:
            pygame.draw.rect(self.gameWindow, (0,255,0), (i.x, i.y, 20, 20), 0)
            
        if self.apple == 3:
            self.addApple()

        if self.apple != None:
            pygame.draw.rect(self.gameWindow, (255,0,0), (self.apple.x, self.apple.y, 20, 20), 0)

        self.snakeCollision()
       
    def isGameOver(self):
        pass
