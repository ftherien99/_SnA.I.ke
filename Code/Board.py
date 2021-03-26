import pygame
import numpy as np
from Snake import Snake

class Board:
    def __init__(self, game):
        self.ticClock = pygame.time.Clock()
        self.apple = None
        self.width = 1300  
        self.height = 800 
        self.scaledWidth = self.width//20
        self.scaledHeight = self.height//20
        self.snake = Snake(20, self.width/2, self.height/2)
        #self.boardArray = np.full((650, 400),'E')
        self.game = game
        self.gameWindow = game.gameWindow

       #for i in range(self.snake.body.length):
       #    if i == 0:
       #        self.boardArray[self.width//2, self.height//2] = 'H'
       #        pygame.draw
       #    else:
       #        self.boardArray[self.width//2 + 1, self.height//2] = 'B'

        
      
        

    def addApple(self):
        pygame.draw.rect(self.gameWindow, (255,0,0), (710, 340, 20, 20), 2)

    def removeApple():
        pass

    def snakeCollision(self):
        pass

    def tic(self):
        if self.snake.currentDirection != "paused":
            self.snake.body.rotate(self.snake.snakeXMovement,self.snake.snakeYMovement)
        for i in self.snake.body.deque:
            pygame.draw.rect(self.gameWindow, (0,255,0), (i.x, i.y, 20, 20), 2)
            

        #self.testX += self.snake.snakeXMovement
        #self.testY += self.snake.snakeYMovement
        self.addApple()
       
       
        
        
        
        

    def isGameOver(self):
        pass
