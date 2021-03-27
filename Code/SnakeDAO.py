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
            if self.cursor is not None:
                print("Database connection established")

    def dbCloseConnection(self):
        self.cursor.close()     
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
            print("Error while fetching data")

    def saveHighscore(self,gameType, highscore):
        query = "UPDATE highscores SET " + gameType + " = %s WHERE id = 1"
        try:
            self.cursor.execute(query,[highscore])

            self.connection.commit()
        except:
            print("Faield to save data")