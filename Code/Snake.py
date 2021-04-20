import pygame
from collections import deque
from Point import Point

class Snake:
    def __init__(self, startPointX, startPointY):
        self.snakeStartPoint = Point(startPointX, startPointY)
        self.headcolor = None
        self.bodyColor = None
        self.body = Body(self.snakeStartPoint)
        self.snakeXMovement = -1
        self.snakeYMovement = 0
        self.snakeController = SnakeController(self)
        self.currentDirection = "left"


class Body:
    def __init__(self, startingPoint):
        self.length = 1
        self.deque = deque([startingPoint])

        for i in range(self.length):
            x = self.deque[i].x
            y = self.deque[i].y

            x += 1

            self.deque.append(Point(x, y))

    def rotate(self, xSpeed, ySpeed):
        temp = self.deque.pop()

        temp.x = self.deque[0].x
        temp.y = self.deque[0].y

        temp.x += xSpeed
        temp.y += ySpeed

        self.deque.appendleft(temp)

    def grow(self, direction):
        incr = 1
        
        if self.length == 1:
            incr = 2
        
        newPoint = Point(self.deque[self.length].x,self.deque[self.length].y)

        if direction == "up":
            newPoint.y -= incr
        elif direction == "down":
            newPoint.y += incr
        elif direction == "left":
            newPoint.x -= incr
        elif direction == "right":
            newPoint.x += incr

        self.deque.append(newPoint)
        self.length += 1
        print(self.deque[0].x, self.deque[0].y,self.deque[1].x,self.deque[1].y ,self.deque[2].x, self.deque[2].y)
        
    
        

class SnakeController:
    def __init__(self, snake):
        self.snake = snake
        self.lastTicks = pygame.time.get_ticks()

    def changeDirection(self, direction):
        
        #gachette

        if direction == "up" and self.snake.currentDirection != "down":
            self.snake.snakeYMovement = -1
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
            
            
        elif direction == "down" and self.snake.currentDirection != "up":
            self.snake.snakeYMovement = 1
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "left" and self.snake.currentDirection != "right":
            self.snake.snakeXMovement = -1
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "right" and self.snake.currentDirection != "left":
            self.snake.snakeXMovement = 1
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "paused":
            self.snake.snakeXMovement = 0
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
