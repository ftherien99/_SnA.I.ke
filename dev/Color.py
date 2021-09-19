class Color:
    def __init__(self):
        self.darkGreen = (11, 59, 24)
        self.lightGreen = (0, 255, 10)
        self.red = (255, 0, 0)
        self.yellow = (246, 255, 0)
        self.orange = (255, 119, 0)
        self.purple = (119, 0, 255)
        self.pink = (255, 0, 217)
        self.lightBlue = (0, 98, 255)
        self.darkBlue = (21, 0, 255)
        self.white = (255, 255, 255)

    def getColors(self):
        colors = [self.darkGreen,self.lightGreen,self.red,self.yellow,self.orange,self.purple,self.pink,self.lightBlue,self.darkBlue,self.white]
        return colors

    def getColorNames(self):
        colorNames = ["darkGreen","lightGreen","red","yellow","orange","purple","pink","lightBlue","darkBlue","white"]
        return colorNames