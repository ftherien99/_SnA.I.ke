import psycopg2
from DAO import DAO

class SnakeDAO(DAO):
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

            self.createTables()

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
        print("save")
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


    def saveEpisode(self, steps, time, score, reward):
        query = "INSERT INTO episodes (number_of_steps, episode_time_sec, episode_score, episode_reward) VALUES (%s,%s,%s,%s)"

        try:
            self.cursor.execute(query,(steps,time,score,reward))
            self.connection.commit()
        except:
            print("Failed to save episode")


    def getEpisodes(self):
        query = "SELECT episode_number FROM episodes"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        episodes = []
        for row in records:
            episodes.append(row)

        return episodes

    def getEpisodeSteps(self):
        query = "SELECT number_of_steps FROM episodes"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        steps = []
        for row in records:
            steps.append(row)

        return steps

    def getEpisodeTime(self):
        query = "SELECT episode_time_sec FROM episodes"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        time = []
        for row in records:
            time.append(row)

        return time

    def getEpisodeScore(self):
        query = "SELECT episode_score FROM episodes"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        scores = []
        for row in records:
            scores.append(row)

        return scores

    def getEpisodeReward(self):
        query = "SELECT episode_reward FROM episodes"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        rewards = []
        for row in records:
            rewards.append(row)

        return rewards


    def createTables(self):
        try:
            query = "SELECT * FROM highscores"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
        except :
            self.connection.rollback()
            print("Creating table highscores")
            createQuery = """CREATE TABLE highscores(
                            id SERIAL NOT NULL PRIMARY KEY,
                            small_board_play       INTEGER,
                            large_board_play       INTEGER,
                            small_board_ai         INTEGER,
                            large_board_ai         INTEGER)"""
                          
            insertQuery = """INSERT INTO highscores (small_board_play, large_board_play, small_board_ai, large_board_ai)
                            VALUES (%s,%s,%s,%s)"""
                          
            
           
            self.cursor.execute(createQuery)
            self.cursor.execute(insertQuery,(0,0,0,0))
            self.connection.commit()


        try:
            query = "SELECT * FROM colors"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
        except:
            self.connection.rollback()
            print("Creating table colors")
            createQuery = """CREATE TABLE colors(
                                id SERIAL NOT NULL PRIMARY KEY,
                                head_color       INTEGER,
                                body_color       INTEGER,
                                apple_color      INTEGER)"""
                    
            insertQuery =  """INSERT INTO colors (head_color, body_color, apple_color)
                                VALUES (%s,%s,%s)"""
                     
            self.cursor.execute(createQuery)
            self.cursor.execute(insertQuery,(0,0,0))
            self.connection.commit()


        try:
            query = "SELECT * FROM episodes"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
        except:
            self.connection.rollback()
            print("Creating table episodes")
            createQuery = """CREATE TABLE episodes(
                                episode_number SERIAL NOT NULL PRIMARY KEY,
                                number_of_steps                    INTEGER,
                                episode_time_sec                   INTEGER,
                                episode_score                      INTEGER,
                                episode_reward                     NUMERIC(6,2))"""
                     
            self.cursor.execute(createQuery)
            self.connection.commit()
