import pygame
from collections import deque
from Point import Point

class Snake:
    def __init__(self, speed, startPointX, startPointY):
        self.snakeStartPoint = Point(startPointX, startPointY)
        self.headcolor = None
        self.bodyColor = None
        self.body = Body(self.snakeStartPoint)
        self.speed = speed
        self.snakeXMovement = -1 * self.speed
        self.snakeYMovement = 0
        self.snakeController = SnakeController(self)
        self.currentDirection = "left"


class Body:
    def __init__(self, startingPoint):
        self.length = 10
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

        newPoint = Point(self.deque[self.length].x,self.deque[self.length].y)

        if direction == "up":
            newPoint.y -= 1
        elif direction == "down":
            newPoint.y += 1
        elif direction == "left":
            newPoint.x -= 1
        elif direction == "right":
            newPoint.x += 1

        self.deque.append(newPoint)
        self.length += 1
        
    
        

class SnakeController:
    def __init__(self, snake):
        self.snake = snake
        self.lastTicks = pygame.time.get_ticks()

    def changeDirection(self, direction):
        

        if direction == "up" and self.snake.currentDirection != "down":
            self.snake.snakeYMovement = -self.snake.speed
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
            
            
        elif direction == "down" and self.snake.currentDirection != "up":
            self.snake.snakeYMovement = self.snake.speed
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "left" and self.snake.currentDirection != "right":
            self.snake.snakeXMovement = -self.snake.speed
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "right" and self.snake.currentDirection != "left":
            self.snake.snakeXMovement = self.snake.speed
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "paused":
            self.snake.snakeXMovement = 0
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction