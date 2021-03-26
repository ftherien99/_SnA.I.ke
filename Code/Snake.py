import pygame
from collections import deque

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

    def grow(self):
        pass




class Body:
    def __init__(self, startingPoint):
        self.length = 10
        self.deque = deque([startingPoint])

        for i in range(self.length):
            print(i)
            x = self.deque[i].x
            y = self.deque[i].y

            x += 20

            self.deque.append(Point(x, y))

    def rotate(self, xSpeed, ySpeed):
        temp = self.deque.pop()

        temp.x = self.deque[0].x
        temp.y = self.deque[0].y

        temp.x += xSpeed
        temp.y += ySpeed

        self.deque.appendleft(temp)



class Point:
    def __init__(self,x ,y):
        self.x = x
        self.y = y






class SnakeController:
    def __init__(self, snake):
        self.snake = snake

    def changeDirection(self, direction):
        
        if direction == "up" and self.snake.currentDirection != "down":
            self.snake.snakeYMovement = -1 * self.snake.speed
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
            
            
        elif direction == "down" and self.snake.currentDirection != "up":
            self.snake.snakeYMovement = 1 * self.snake.speed
            self.snake.snakeXMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "left" and self.snake.currentDirection != "right":
            self.snake.snakeXMovement = -1 * self.snake.speed
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "right" and self.snake.currentDirection != "left":
            self.snake.snakeXMovement = 1 * self.snake.speed
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
           

        elif direction == "paused":
            self.snake.snakeXMovement = 0
            self.snake.snakeYMovement = 0
            self.snake.currentDirection = direction
