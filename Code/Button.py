import pygame
pygame.init()

#RÉFÉRENCES: https://youtu.be/4_9twnEduFA

class Button:
    def __init__(self, height, width, posX, posY, color, text):
        self.height = height
        self.width = width
        self.posX = posX
        self.posY = posY
        self.color = color
        self.text = text
        
        
      
    
    def drawButton(self, window):
        pygame.draw.rect(window, self.color, (self.posX, self.posY, self.width, self.height), 0)
        textFont = pygame.font.SysFont("arial", 24)
        buttonText = textFont.render(self.text, 1, (0,0,0))
        window.blit(buttonText, (self.posX + (self.width/2 - buttonText.get_width()/2), self.posY + (self.height/2 - buttonText.get_height()/2)))

    def clicked(self, mousePos):
        if mousePos[0] > self.posX and mousePos[0] < self.posX + self.width:
            if mousePos[1] > self.posY and mousePos[1] < self.posY + self.height:
                return True
                
        
        return False
