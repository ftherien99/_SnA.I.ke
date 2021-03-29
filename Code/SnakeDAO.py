import psycopg2

class SnakeDAO:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def dbConnection(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="snake",
                user="postgres",
                password="123"
            )

            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:
                print("Database connection established")

    def dbCloseConnection(self):     
        self.connection.close()
        print("Database connection closed")

    def getHighscore(self,gameType):
        try:
            query = "SELECT * FROM highscores"
            self.cursor.execute(query)
            records = self.cursor.fetchall()

            for row in records:
                if gameType == "small_board_play":
                    print(row[1])
                    return row[1]
                elif gameType == "large_board_play":
                    print(row[2])
                    return row[2]
                elif gameType == "small_board_ai":
                    print(row[3])
                    return row[3]
                elif gameType == "large_board_ai":
                    print(row[4])
                    return row[4]
           
        except:
            print("Error while fetching highscore data")


    def saveHighscore(self,gameType, highscore):
        query = "UPDATE highscores SET " + gameType + " = %s WHERE id = 1"
        try:
            self.cursor.execute(query,[highscore])

            self.connection.commit()
        except:
            print("Failed to save highscore data")



    def getColors(self, gameObject):
        try:
            query = "SELECT * FROM colors"
            self.cursor.execute(query)
            records = self.cursor.fetchall()

            #transformation int to RGB: https://stackoverflow.com/questions/2262100/rgb-int-to-rgb-python
            for row in records:
                if gameObject == "head":
                    color = (row[1] // 256 // 256 % 256, row[1] // 256 % 256, row[1] % 256)
                    return color
                elif gameObject == "body":
                    color = (row[2] // 256 // 256 % 256, row[2] // 256 % 256, row[2] % 256)
                    return color
                elif gameObject == "apple":
                    color = (row[3] // 256 // 256 % 256, row[3] // 256 % 256, row[3] % 256)
                    return color
           
        except:
            print("Error while fetching color data")



    def saveColors(self,headColor, bodyColor, appleColor):
        headColorInt = (headColor[0] * 256 * 256) + (headColor[1] * 256) + headColor[2]
        bodyColorInt = (bodyColor[0] * 256 * 256) + (bodyColor[1] * 256) + bodyColor[2]
        appleColorInt = (appleColor[0] * 256 * 256) + (appleColor[1] * 256) + appleColor[2]

        query = "UPDATE colors SET head_color = %s, body_color = %s, apple_color = %s WHERE id = 1"
        try:
            self.cursor.execute(query,(headColorInt, bodyColorInt, appleColorInt))
            self.connection.commit()
        except:
            print("Failed to save color data")
